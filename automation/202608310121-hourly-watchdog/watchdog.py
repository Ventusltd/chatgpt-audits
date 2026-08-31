#!/usr/bin/env python3
"""Hourly GitHub Actions supervisor for the quarantined audit programme.

REVIEW STATUS: UNREVIEWED.

The supervisor may re-run the latest failed audit workflow in
Ventusltd/chatgpt-audits only. Every other Ventus repository is observed
read-only. Product Pages noise and historical/cancelled runs are retained as
evidence but are not described as unresolved audit failures.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

AUDIT_REPOSITORY = "Ventusltd/chatgpt-audits"
REVIEW_STATUS = "UNREVIEWED"
LONDON = ZoneInfo("Europe/London")
ACTIVE_STATUSES = {"queued", "in_progress", "waiting", "requested", "pending"}
FAILED_CONCLUSIONS = {
    "failure",
    "cancelled",
    "timed_out",
    "action_required",
    "startup_failure",
}
TARGET_AUDIT_WORKFLOWS = {
    "202608310052 five-hour quarantined cross-repo study",
    "202608310116 overnight audit swarm",
    "202608310121 hourly audit watchdog",
}
EXCLUDED_RERUN_WORKFLOWS = {
    "202608310122 audit failure auto-repair",
    "pages build and deployment",
}
REPOSITORIES = [
    AUDIT_REPOSITORY,
    "Ventusltd/pipelinenews",
    "Ventusltd/companies",
    "Ventusltd/gridatlas",
    "Ventusltd/data-gridatlas",
    "Ventusltd/globalgrid2050",
    "Ventusltd/spiders",
    "Ventusltd/cvaa",
    "Ventusltd/data-centres-gb",
    "Ventusltd/data-gb-electricity",
]


@dataclass(frozen=True)
class ApiResult:
    ok: bool
    status: int
    payload: Any
    error: str | None = None


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def github_request(
    method: str,
    endpoint: str,
    token: str,
    payload: dict[str, Any] | None = None,
    *,
    attempts: int = 3,
) -> ApiResult:
    url = endpoint if endpoint.startswith("https://") else f"https://api.github.com{endpoint}"
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "chatgpt-audits-hourly-watchdog/202608310121-v2",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    last_error = None
    for attempt in range(1, attempts + 1):
        request = urllib.request.Request(url, data=body, method=method, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read()
                decoded: Any = None
                if raw:
                    decoded = json.loads(raw.decode("utf-8"))
                return ApiResult(True, response.status, decoded)
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace")
            last_error = f"HTTP {exc.code}: {raw[:700]}"
            if exc.code not in {429, 500, 502, 503, 504} or attempt == attempts:
                return ApiResult(False, exc.code, None, last_error)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
            if attempt == attempts:
                return ApiResult(False, 0, None, last_error)
        time.sleep(attempt * 2)
    return ApiResult(False, 0, None, last_error or "unknown API error")


def threshold_minutes(name: str) -> int:
    lowered = name.lower()
    if "five-hour" in lowered:
        return 390
    if "overnight audit swarm" in lowered:
        return 120
    if "hourly audit watchdog" in lowered:
        return 35
    if "failure auto-repair" in lowered:
        return 25
    return 100


def is_pages_noise(run: dict[str, Any]) -> bool:
    name = str(run.get("name") or "").lower()
    path = str(run.get("path") or "").lower()
    return name == "pages build and deployment" or path.startswith("dynamic/pages/")


def compact_run(run: dict[str, Any], now: datetime) -> dict[str, Any]:
    created = parse_time(run.get("created_at")) or now
    updated = parse_time(run.get("updated_at")) or created
    return {
        "run_id": run.get("id"),
        "name": str(run.get("name") or run.get("path") or "unknown"),
        "path": run.get("path"),
        "event": run.get("event"),
        "head_sha": run.get("head_sha"),
        "status": run.get("status"),
        "conclusion": run.get("conclusion"),
        "run_attempt": run.get("run_attempt"),
        "created_at": run.get("created_at"),
        "updated_at": run.get("updated_at"),
        "age_minutes": round((now - created).total_seconds() / 60, 1),
        "quiet_minutes": round((now - updated).total_seconds() / 60, 1),
        "html_url": run.get("html_url"),
    }


def job_evidence(repository: str, run_id: int, token: str) -> dict[str, Any]:
    result = github_request(
        "GET",
        f"/repos/{repository}/actions/runs/{run_id}/jobs?per_page=100&filter=latest",
        token,
    )
    if not result.ok:
        return {"api_error": result.error, "jobs": []}
    jobs = []
    for job in (result.payload or {}).get("jobs", []):
        failed_steps = [
            {
                "number": step.get("number"),
                "name": step.get("name"),
                "status": step.get("status"),
                "conclusion": step.get("conclusion"),
            }
            for step in job.get("steps", [])
            if step.get("conclusion") in FAILED_CONCLUSIONS
        ]
        if job.get("conclusion") in FAILED_CONCLUSIONS or failed_steps:
            jobs.append(
                {
                    "job_id": job.get("id"),
                    "name": job.get("name"),
                    "status": job.get("status"),
                    "conclusion": job.get("conclusion"),
                    "started_at": job.get("started_at"),
                    "completed_at": job.get("completed_at"),
                    "failed_steps": failed_steps,
                }
            )
    return {"api_error": None, "jobs": jobs}


def request_rerun(repository: str, run: dict[str, Any], token: str) -> dict[str, Any]:
    run_id = int(run["id"])
    conclusion = str(run.get("conclusion") or "")
    endpoint = (
        f"/repos/{repository}/actions/runs/{run_id}/rerun-failed-jobs"
        if conclusion == "failure"
        else f"/repos/{repository}/actions/runs/{run_id}/rerun"
    )
    result = github_request("POST", endpoint, token)
    return {
        "requested": result.ok,
        "endpoint": endpoint,
        "http_status": result.status,
        "error": result.error,
    }


def classify_failure(repository: str, run: dict[str, Any], latest_for_name: bool) -> str:
    if is_pages_noise(run):
        return "pages_platform_observation"
    if repository != AUDIT_REPOSITORY:
        return "product_repository_observation"
    name = str(run.get("name") or run.get("path") or "unknown")
    if name in EXCLUDED_RERUN_WORKFLOWS:
        return "audit_nonrepairable_observation"
    if name in TARGET_AUDIT_WORKFLOWS and latest_for_name:
        return "audit_actionable_failure"
    return "audit_historical_failure"


def summarise_repository(
    repository: str,
    token: str,
    now: datetime,
    since: datetime,
    *,
    max_reruns_remaining: list[int],
) -> dict[str, Any]:
    result = github_request(
        "GET",
        f"/repos/{repository}/actions/runs?per_page=100&exclude_pull_requests=true",
        token,
    )
    summary: dict[str, Any] = {
        "repository": repository,
        "classification": "observed",
        "api_error": None,
        "runs_examined": 0,
        "recent": [],
        "active": [],
        "successful": [],
        "failed": [],
        "stalled": [],
        "reruns": [],
    }
    if not result.ok:
        summary["api_error"] = result.error
        return summary

    runs = []
    for run in (result.payload or {}).get("workflow_runs", []):
        created = parse_time(run.get("created_at"))
        updated = parse_time(run.get("updated_at"))
        if created is None:
            continue
        if created >= since or (run.get("status") in ACTIVE_STATUSES and (updated or created) >= since):
            runs.append(run)
    runs.sort(
        key=lambda row: parse_time(row.get("created_at"))
        or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )
    summary["runs_examined"] = len(runs)

    latest_ids_by_name: dict[str, Any] = {}
    for run in runs:
        name = str(run.get("name") or run.get("path") or "unknown")
        latest_ids_by_name.setdefault(name, run.get("id"))

    for run in runs:
        compact = compact_run(run, now)
        name = compact["name"]
        compact["latest_for_name"] = latest_ids_by_name.get(name) == compact["run_id"]
        summary["recent"].append(compact)

        if run.get("status") in ACTIVE_STATUSES:
            summary["active"].append(compact)
            threshold = threshold_minutes(name)
            queued_stall = run.get("status") == "queued" and compact["age_minutes"] > 35
            running_stall = run.get("status") == "in_progress" and compact["age_minutes"] > threshold
            if queued_stall or running_stall:
                summary["stalled"].append(
                    {
                        **compact,
                        "classification": "inferred",
                        "threshold_minutes": 35 if queued_stall else threshold,
                        "reason": "queued beyond threshold"
                        if queued_stall
                        else "running beyond workflow-specific threshold",
                    }
                )

        if run.get("conclusion") == "success":
            summary["successful"].append(compact)

        if run.get("conclusion") in FAILED_CONCLUSIONS:
            failure_class = classify_failure(repository, run, bool(compact["latest_for_name"]))
            failure = {
                **compact,
                "failure_class": failure_class,
                "jobs": (
                    job_evidence(repository, int(run["id"]), token)
                    if repository == AUDIT_REPOSITORY and not is_pages_noise(run)
                    else {"api_error": None, "jobs": [], "detail_policy": "metadata-only"}
                ),
                "product_repository_mutation_allowed": False,
            }
            summary["failed"].append(failure)
            eligible = (
                failure_class == "audit_actionable_failure"
                and name in TARGET_AUDIT_WORKFLOWS
                and name not in EXCLUDED_RERUN_WORKFLOWS
                and int(run.get("run_attempt") or 1) < 3
                and max_reruns_remaining[0] > 0
            )
            if eligible:
                rerun = request_rerun(repository, run, token)
                rerun.update(
                    {
                        "run_id": run["id"],
                        "name": name,
                        "previous_attempt": run.get("run_attempt"),
                    }
                )
                summary["reruns"].append(rerun)
                if rerun["requested"]:
                    max_reruns_remaining[0] -= 1

    return summary


def latest_workflow_state(audit_runs: dict[str, Any], name: str) -> dict[str, Any]:
    rows = [row for row in audit_runs["recent"] if row["name"] == name]
    if not rows:
        return {"state": "NOT_SEEN_IN_LOOKBACK", "run": None, "classification": "unknown"}
    latest = rows[0]
    if latest["status"] in ACTIVE_STATUSES:
        state = "RUNNING"
    elif latest["conclusion"] == "success":
        state = "COMPLETED_SUCCESS"
    elif latest["conclusion"] in FAILED_CONCLUSIONS:
        state = "FAILED"
    else:
        state = "COMPLETED_OTHER"
    return {"state": state, "run": latest, "classification": "observed"}


def markdown_report(report: dict[str, Any]) -> str:
    timer = report["timer_state"]
    totals = report["totals"]
    lines = [
        "# Hourly audit watchdog",
        "",
        "> **REVIEW STATUS: UNREVIEWED**  ",
        "> Classification: mixed `observed` / `inferred`  ",
        "> Product repositories were inspected read-only. Automatic re-runs are restricted to the latest failed `Ventusltd/chatgpt-audits` workflow.",
        "",
        f"Checked: `{report['checked_at_london']}` Europe/London  ",
        f"Five-hour controller: **{timer['five_hour']['state']}**  ",
        f"Overnight swarm: **{timer['swarm']['state']}**  ",
        f"Actionable audit failures: **{totals['audit_actionable_failures']}**  ",
        f"Automatic audit re-runs requested: **{totals['reruns_requested']}**  ",
        f"Product failures observed read-only: **{totals['product_failures_observed']}**  ",
        f"Pages/platform observations separated from actionable failures: **{totals['pages_platform_observations']}**  ",
        f"Potentially stalled runs: **{totals['stalled_runs']}**",
        "",
        "## Repository status",
        "",
        "| Repository | Active | Audit-actionable | Product observations | Pages noise | Stalled | Re-runs | API |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for repo in report["repositories"]:
        classes = [row["failure_class"] for row in repo["failed"]]
        lines.append(
            f"| `{repo['repository']}` | {len(repo['active'])} | "
            f"{classes.count('audit_actionable_failure')} | "
            f"{classes.count('product_repository_observation')} | "
            f"{classes.count('pages_platform_observation')} | "
            f"{len(repo['stalled'])} | "
            f"{sum(1 for row in repo['reruns'] if row['requested'])} | "
            f"{'ERROR' if repo['api_error'] else 'OK'} |"
        )

    actionable = [
        failure
        for repo in report["repositories"]
        for failure in repo["failed"]
        if failure["failure_class"] == "audit_actionable_failure"
    ]
    lines.extend(["", "## Actionable audit failures"])
    if not actionable:
        lines.extend(["", "No latest audit workflow is presently in a repair-eligible failed state."])
    else:
        for failure in actionable:
            failed_jobs = failure["jobs"].get("jobs", [])
            job_text = ", ".join(job["name"] for job in failed_jobs) or "job detail unavailable"
            lines.extend(
                [
                    "",
                    f"- Run `{failure['run_id']}` — **{failure['conclusion']}**, attempt "
                    f"{failure['run_attempt']}: {failure['name']}; {job_text}.",
                ]
            )

    product_observations = [
        (repo["repository"], failure)
        for repo in report["repositories"]
        for failure in repo["failed"]
        if failure["failure_class"] == "product_repository_observation"
    ]
    lines.extend(["", "## Product-repository observations"])
    if not product_observations:
        lines.extend(["", "No non-Pages product failures were observed in the bounded lookback."])
    else:
        lines.append("")
        lines.append(
            f"Observed `{len(product_observations)}` non-Pages product failures/cancellations. They are evidence only; this audit controller has no mutation or dispatch authority there."
        )
        for repository, failure in product_observations[:12]:
            lines.append(
                f"- `{repository}` run `{failure['run_id']}` — {failure['conclusion']}: {failure['name']}."
            )

    lines.extend(
        [
            "",
            "## Repair boundary",
            "",
            "- Only the latest failed audit workflow may be re-run, up to attempt 3.",
            "- A newer active or successful run suppresses repair of an older failed run with the same workflow name.",
            "- Product-repository runs are evidence only: no dispatch, re-run, commit, release or Pages mutation is allowed.",
            "- Pages build/deployment noise is counted separately and is not labelled an unresolved audit failure.",
            "- Deterministic source defects are sent to the separate repair diagnosis workflow; this watchdog does not rewrite source from logs.",
            "- Absence from this bounded lookback is not evidence that no older failure exists.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--hours-back", type=int, default=12)
    parser.add_argument("--max-reruns", type=int, default=3)
    args = parser.parse_args(argv)

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    if not token:
        print("GH_TOKEN or GITHUB_TOKEN is required", file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=max(1, args.hours_back))
    reruns_remaining = [max(0, args.max_reruns)]
    repositories = [
        summarise_repository(repo, token, now, since, max_reruns_remaining=reruns_remaining)
        for repo in REPOSITORIES
    ]

    audit_runs = next(row for row in repositories if row["repository"] == AUDIT_REPOSITORY)
    timer_state = {
        "five_hour": latest_workflow_state(
            audit_runs, "202608310052 five-hour quarantined cross-repo study"
        ),
        "swarm": latest_workflow_state(audit_runs, "202608310116 overnight audit swarm"),
    }

    failures = [failure for repo in repositories for failure in repo["failed"]]
    report = {
        "schema": "chatgpt-audits.hourly-watchdog.v2",
        "generation": "202608310121",
        "review_status": REVIEW_STATUS,
        "classification": "observed",
        "checked_at": now.isoformat().replace("+00:00", "Z"),
        "checked_at_london": now.astimezone(LONDON).isoformat(),
        "lookback_hours": args.hours_back,
        "source_policy": {
            "write_boundary": AUDIT_REPOSITORY,
            "audit_rerun_limit": 3,
            "product_repository_actions": "READ_ONLY",
            "absence_is_evidence": False,
        },
        "timer_state": timer_state,
        "repositories": repositories,
    }
    report["totals"] = {
        "active_runs": sum(len(row["active"]) for row in repositories),
        "audit_actionable_failures": sum(
            failure["failure_class"] == "audit_actionable_failure" for failure in failures
        ),
        "audit_historical_failures": sum(
            failure["failure_class"] == "audit_historical_failure" for failure in failures
        ),
        "audit_nonrepairable_observations": sum(
            failure["failure_class"] == "audit_nonrepairable_observation" for failure in failures
        ),
        "product_failures_observed": sum(
            failure["failure_class"] == "product_repository_observation" for failure in failures
        ),
        "pages_platform_observations": sum(
            failure["failure_class"] == "pages_platform_observation" for failure in failures
        ),
        "stalled_runs": sum(len(row["stalled"]) for row in repositories),
        "reruns_requested": sum(
            1 for row in repositories for rerun in row["reruns"] if rerun["requested"]
        ),
        "api_errors": sum(1 for row in repositories if row["api_error"]),
    }

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "watchdog.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output / "WATCHDOG.md").write_text(markdown_report(report), encoding="utf-8")
    print(json.dumps(report["totals"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
