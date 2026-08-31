#!/usr/bin/env python3
"""Hourly GitHub Actions supervisor for the quarantined audit programme.

REVIEW STATUS: UNREVIEWED.

The supervisor may re-run recent failed jobs in Ventusltd/chatgpt-audits only.
Every other Ventus repository is observed read-only. It never dispatches or
mutates a product repository.
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
        "User-Agent": "chatgpt-audits-hourly-watchdog/202608310121",
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
        "active": [],
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
        if created >= since or (run.get("status") in {"queued", "in_progress"} and (updated or created) >= since):
            runs.append(run)
    summary["runs_examined"] = len(runs)

    for run in runs:
        name = str(run.get("name") or run.get("path") or "unknown")
        created = parse_time(run.get("created_at")) or now
        updated = parse_time(run.get("updated_at")) or created
        age_minutes = round((now - created).total_seconds() / 60, 1)
        quiet_minutes = round((now - updated).total_seconds() / 60, 1)
        compact = {
            "run_id": run.get("id"),
            "name": name,
            "path": run.get("path"),
            "event": run.get("event"),
            "head_sha": run.get("head_sha"),
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "run_attempt": run.get("run_attempt"),
            "created_at": run.get("created_at"),
            "updated_at": run.get("updated_at"),
            "age_minutes": age_minutes,
            "quiet_minutes": quiet_minutes,
            "html_url": run.get("html_url"),
        }
        if run.get("status") in {"queued", "in_progress", "waiting", "requested", "pending"}:
            summary["active"].append(compact)
            threshold = threshold_minutes(name)
            queued_stall = run.get("status") == "queued" and age_minutes > 35
            running_stall = run.get("status") == "in_progress" and age_minutes > threshold
            if queued_stall or running_stall:
                summary["stalled"].append(
                    {
                        **compact,
                        "classification": "inferred",
                        "threshold_minutes": 35 if queued_stall else threshold,
                        "reason": "queued beyond threshold" if queued_stall else "running beyond workflow-specific threshold",
                    }
                )

        if run.get("conclusion") in FAILED_CONCLUSIONS:
            failure = {
                **compact,
                "jobs": job_evidence(repository, int(run["id"]), token),
                "product_repository_mutation_allowed": repository == AUDIT_REPOSITORY,
            }
            summary["failed"].append(failure)
            eligible = (
                repository == AUDIT_REPOSITORY
                and name in TARGET_AUDIT_WORKFLOWS
                and name not in EXCLUDED_RERUN_WORKFLOWS
                and int(run.get("run_attempt") or 1) < 3
                and max_reruns_remaining[0] > 0
            )
            if eligible:
                rerun = request_rerun(repository, run, token)
                rerun.update({"run_id": run["id"], "name": name, "previous_attempt": run.get("run_attempt")})
                summary["reruns"].append(rerun)
                if rerun["requested"]:
                    max_reruns_remaining[0] -= 1

    return summary


def markdown_report(report: dict[str, Any]) -> str:
    timer = report["timer_state"]
    lines = [
        "# Hourly audit watchdog",
        "",
        "> **REVIEW STATUS: UNREVIEWED**  ",
        "> Classification: mixed `observed` / `inferred`  ",
        "> Product repositories were inspected read-only. Automatic re-runs are restricted to `Ventusltd/chatgpt-audits`.",
        "",
        f"Checked: `{report['checked_at_london']}` Europe/London  ",
        f"Audit timer: **{timer['five_hour']}**  ",
        f"Overnight swarm: **{timer['swarm']}**  ",
        f"Automatic re-runs requested this check: **{report['totals']['reruns_requested']}**  ",
        f"Unresolved recent failures observed: **{report['totals']['failed_runs']}**  ",
        f"Potentially stalled runs: **{report['totals']['stalled_runs']}**",
        "",
        "## Repository status",
        "",
        "| Repository | Active | Failed | Stalled | Re-runs | API |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for repo in report["repositories"]:
        lines.append(
            f"| `{repo['repository']}` | {len(repo['active'])} | {len(repo['failed'])} | "
            f"{len(repo['stalled'])} | {sum(1 for row in repo['reruns'] if row['requested'])} | "
            f"{'ERROR' if repo['api_error'] else 'OK'} |"
        )

    failures = [
        (repo["repository"], failure)
        for repo in report["repositories"]
        for failure in repo["failed"]
    ]
    lines.extend(["", "## Recent failed actions"])
    if not failures:
        lines.append("")
        lines.append("No failed, cancelled or timed-out runs were observed in the bounded lookback.")
    else:
        for repository, failure in failures[:30]:
            failed_jobs = failure["jobs"].get("jobs", [])
            job_text = ", ".join(job["name"] for job in failed_jobs) or "job detail unavailable"
            lines.extend(
                [
                    "",
                    f"- `{repository}` run `{failure['run_id']}` — **{failure['conclusion']}**, "
                    f"attempt {failure['run_attempt']}: {failure['name']}; {job_text}.",
                ]
            )

    lines.extend(
        [
            "",
            "## Repair boundary",
            "",
            "- Failed audit jobs may be re-run up to attempt 3.",
            "- Product-repository runs are evidence only: no dispatch, re-run, commit, release or Pages mutation is allowed.",
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
    five_hour = [
        row for row in audit_runs["active"]
        if row["name"] == "202608310052 five-hour quarantined cross-repo study"
    ]
    swarm = [
        row for row in audit_runs["active"]
        if row["name"] == "202608310116 overnight audit swarm"
    ]

    report = {
        "schema": "chatgpt-audits.hourly-watchdog.v1",
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
        "timer_state": {
            "five_hour": "RUNNING" if five_hour else "NOT_CURRENTLY_ACTIVE",
            "swarm": "RUNNING" if swarm else "NOT_CURRENTLY_ACTIVE",
            "classification": "observed",
        },
        "repositories": repositories,
    }
    report["totals"] = {
        "active_runs": sum(len(row["active"]) for row in repositories),
        "failed_runs": sum(len(row["failed"]) for row in repositories),
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
