#!/usr/bin/env python3
"""Bounded same-repository GitHub Actions watchdog for the overnight audit.

REVIEW STATUS: UNREVIEWED.

The watchdog may only re-run failed jobs or dispatch the current default-branch
version of explicitly allowlisted workflows in Ventusltd/chatgpt-audits.
It never modifies or dispatches a product repository.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo

REVIEW_STATUS = "UNREVIEWED"
REPOSITORY = "Ventusltd/chatgpt-audits"
WATCHED = {
    "202608310052 five-hour quarantined cross-repo study": "202608310052-five-hour-quarantined-study.yml",
    "202608310116 overnight audit swarm": "202608310116-overnight-audit-swarm.yml",
}
FAILURES = {"failure", "cancelled", "timed_out", "action_required", "stale"}
ACTIVE = {"queued", "in_progress", "waiting", "requested", "pending"}
TRANSIENT_PATTERNS = {
    "github-5xx": re.compile(r"\b(?:500|502|503|504)\b|bad gateway|service unavailable|gateway timeout", re.I),
    "rate-limit": re.compile(r"rate limit|secondary rate|abuse detection", re.I),
    "network": re.compile(
        r"connection (?:reset|refused|timed out)|temporary failure|could not resolve host|network is unreachable|"
        r"remote end hung up|tls handshake timeout|unexpected eof|failed to connect|connection closed",
        re.I,
    ),
    "runner": re.compile(r"runner.*lost communication|runner.*disconnected|hosted runner.*error|machine.*unavailable", re.I),
    "action-download": re.compile(r"failed to download action|unable to download|download.*failed|blobnotfound", re.I),
    "artifact-service": re.compile(r"artifact.*(?:failed|timeout|conflict)|failed to upload artifact|failed to finalize artifact", re.I),
    "git-race": re.compile(r"non-fast-forward|failed to push some refs|reference already exists|cannot lock ref|another git process", re.I),
    "cancelled-operation": re.compile(r"the operation was canceled|the operation was cancelled|job was cancelled", re.I),
}
DETERMINISTIC_PATTERNS = {
    "assertion": re.compile(r"assertionerror|assert\.ok|assertion failed|contract.*mismatch", re.I),
    "syntax": re.compile(r"syntaxerror|yaml.*(?:error|invalid)|unexpected token|indentationerror", re.I),
    "test-failure": re.compile(r"tests? failed|failures?=|quarantine verification failed|process completed with exit code [1-9]", re.I),
    "integrity": re.compile(r"sha(?:256)? .*mismatch|digest mismatch|file closure mismatch|escaped quarantine", re.I),
    "traceback": re.compile(r"traceback \(most recent call last\)", re.I),
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def now_london() -> str:
    return datetime.now(ZoneInfo("Europe/London")).isoformat()


class GitHubAPI:
    def __init__(self, repository: str, token: str) -> None:
        self.repository = repository
        self.base = f"https://api.github.com/repos/{repository}"
        self.token = token

    def request(self, method: str, path: str, payload: Any | None = None, *, raw: bool = False) -> Any:
        url = path if path.startswith("https://") else f"{self.base}{path}"
        data = None
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "chatgpt-audits-actions-watchdog",
        }
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read()
                if raw:
                    return body
                if not body:
                    return None
                return json.loads(body.decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            raise RuntimeError(f"GitHub API {method} {url} -> {exc.code}: {body[:2000]}") from exc

    def main_sha(self) -> str:
        payload = self.request("GET", "/branches/main")
        return str(payload["commit"]["sha"])

    def workflow_runs(self, filename: str, *, per_page: int = 20) -> list[dict[str, Any]]:
        workflow = urllib.parse.quote(filename, safe="")
        payload = self.request("GET", f"/actions/workflows/{workflow}/runs?branch=main&per_page={per_page}")
        return list(payload.get("workflow_runs", []))

    def jobs(self, run_id: int) -> list[dict[str, Any]]:
        payload = self.request("GET", f"/actions/runs/{run_id}/jobs?filter=latest&per_page=100")
        return list(payload.get("jobs", []))

    def job_log(self, job_id: int) -> str:
        try:
            body = self.request("GET", f"/actions/jobs/{job_id}/logs", raw=True)
        except Exception as exc:
            return f"WATCHDOG_LOG_FETCH_ERROR: {exc}"
        return body.decode("utf-8", "replace")[-500_000:]

    def rerun_failed(self, run_id: int) -> None:
        self.request("POST", f"/actions/runs/{run_id}/rerun-failed-jobs", {})

    def dispatch(self, filename: str) -> None:
        workflow = urllib.parse.quote(filename, safe="")
        self.request("POST", f"/actions/workflows/{workflow}/dispatches", {"ref": "main"})


def classify_logs(logs: str) -> dict[str, Any]:
    transient = [name for name, pattern in TRANSIENT_PATTERNS.items() if pattern.search(logs)]
    deterministic = [name for name, pattern in DETERMINISTIC_PATTERNS.items() if pattern.search(logs)]
    if transient and not deterministic:
        classification = "TRANSIENT"
    elif deterministic:
        classification = "DETERMINISTIC_OR_CODE"
    elif logs.strip():
        classification = "UNKNOWN"
    else:
        classification = "NO_LOGS"
    excerpts: list[str] = []
    for line in logs.splitlines():
        if any(pattern.search(line) for pattern in [*TRANSIENT_PATTERNS.values(), *DETERMINISTIC_PATTERNS.values()]):
            compact = " ".join(line.split())
            if compact and compact not in excerpts:
                excerpts.append(compact[:500])
            if len(excerpts) >= 20:
                break
    return {
        "classification": classification,
        "transient_matches": transient,
        "deterministic_matches": deterministic,
        "excerpts": excerpts,
    }


def newest_completed(runs: Iterable[dict[str, Any]]) -> dict[str, Any] | None:
    for run in runs:
        if run.get("status") == "completed":
            return run
    return None


def active_newer_than(runs: Iterable[dict[str, Any]], run: dict[str, Any]) -> list[dict[str, Any]]:
    created = str(run.get("created_at", ""))
    return [
        candidate
        for candidate in runs
        if candidate.get("status") in ACTIVE and str(candidate.get("created_at", "")) >= created
    ]


def inspect_run(api: GitHubAPI, workflow_name: str, filename: str, run: dict[str, Any], main_sha: str) -> dict[str, Any]:
    run_id = int(run["id"])
    result: dict[str, Any] = {
        "workflow": workflow_name,
        "workflow_file": filename,
        "run_id": run_id,
        "run_attempt": int(run.get("run_attempt", 1)),
        "head_sha": run.get("head_sha"),
        "main_sha_at_check": main_sha,
        "status": run.get("status"),
        "conclusion": run.get("conclusion"),
        "created_at": run.get("created_at"),
        "updated_at": run.get("updated_at"),
        "classification": "NOT_FAILED",
        "decision": "NONE",
        "action_taken": False,
        "failed_jobs": [],
    }
    if run.get("conclusion") not in FAILURES:
        return result

    job_logs: list[str] = []
    for job in api.jobs(run_id):
        if job.get("conclusion") not in FAILURES:
            continue
        text = api.job_log(int(job["id"]))
        analysis = classify_logs(text)
        result["failed_jobs"].append(
            {
                "job_id": int(job["id"]),
                "name": job.get("name"),
                "status": job.get("status"),
                "conclusion": job.get("conclusion"),
                **analysis,
            }
        )
        job_logs.append(text)

    combined = classify_logs("\n".join(job_logs))
    result["classification"] = combined["classification"]
    result["transient_matches"] = combined["transient_matches"]
    result["deterministic_matches"] = combined["deterministic_matches"]
    result["excerpts"] = combined["excerpts"]
    return result


def write_report(output: Path, payload: dict[str, Any]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "WATCHDOG.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Overnight GitHub Actions watchdog",
        "",
        f"> **REVIEW STATUS: {REVIEW_STATUS}**  ",
        "> Classification: `observed` for API state; failure causes remain classified below.  ",
        "> This watchdog can act only inside `Ventusltd/chatgpt-audits`.",
        "",
        f"Checked: `{payload['checked_at_london']}`  ",
        f"Main SHA: `{payload['main_sha']}`  ",
        f"Actions taken: **{payload['actions_taken']}**  ",
        f"Unresolved failures: **{payload['unresolved_failures']}**",
        "",
        "| Workflow | Run | Attempt | Conclusion | Classification | Decision |",
        "|---|---:|---:|---|---|---|",
    ]
    for row in payload["checks"]:
        lines.append(
            f"| {row['workflow']} | {row.get('run_id', '—')} | {row.get('run_attempt', '—')} | "
            f"{row.get('conclusion') or row.get('status')} | {row.get('classification')} | {row.get('decision')} |"
        )
    lines.extend(
        [
            "",
            "## Governing boundary",
            "",
            "- No product repository is read with write credentials.",
            "- No product workflow can be dispatched.",
            "- A stale failed audit run is replaced by the current `main` workflow.",
            "- A same-SHA transient failure receives at most one failed-job rerun.",
            "- Deterministic or repeated failures are retained for human/code repair; they are not disguised as green.",
        ]
    )
    (output / "WATCHDOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def event_run(event_path: str | None) -> dict[str, Any] | None:
    if not event_path:
        return None
    path = Path(event_path)
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    run = payload.get("workflow_run")
    return run if isinstance(run, dict) else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--event-path")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repository = os.environ.get("GITHUB_REPOSITORY", REPOSITORY)
    if repository != REPOSITORY:
        raise SystemExit(f"watchdog repository boundary violated: {repository}")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")
    api = GitHubAPI(repository, token)
    main_sha = api.main_sha()
    supplied = event_run(args.event_path or os.environ.get("GITHUB_EVENT_PATH"))

    checks: list[dict[str, Any]] = []
    actions_taken = 0
    unresolved = 0
    for workflow_name, filename in WATCHED.items():
        runs = api.workflow_runs(filename)
        if supplied and supplied.get("name") == workflow_name:
            target = next((row for row in runs if int(row["id"]) == int(supplied["id"])), supplied)
        else:
            target = newest_completed(runs)

        if not target:
            checks.append(
                {
                    "workflow": workflow_name,
                    "workflow_file": filename,
                    "classification": "NO_COMPLETED_RUN",
                    "decision": "NONE",
                    "action_taken": False,
                    "status": "not_observed",
                    "conclusion": None,
                }
            )
            continue

        row = inspect_run(api, workflow_name, filename, target, main_sha)
        if row["conclusion"] in FAILURES:
            newer_active = active_newer_than(runs, target)
            if newer_active:
                row["decision"] = "WAIT_NEWER_ACTIVE_RUN"
                row["newer_active_run_ids"] = [int(item["id"]) for item in newer_active]
            elif row["head_sha"] != main_sha:
                row["decision"] = "DISPATCH_CURRENT_MAIN"
                if not args.dry_run:
                    api.dispatch(filename)
                row["action_taken"] = True
                actions_taken += 1
            elif row["classification"] == "TRANSIENT" and row["run_attempt"] < 2:
                row["decision"] = "RERUN_FAILED_JOBS_ONCE"
                if not args.dry_run:
                    api.rerun_failed(int(row["run_id"]))
                row["action_taken"] = True
                actions_taken += 1
            else:
                row["decision"] = "UNRESOLVED_REPAIR_REQUIRED"
                unresolved += 1
        checks.append(row)

    payload = {
        "schema": "chatgpt-audits.actions-watchdog-report.v1",
        "generation": "202608310125",
        "review_status": REVIEW_STATUS,
        "classification": "observed",
        "checked_at": now_utc(),
        "checked_at_london": now_london(),
        "repository": repository,
        "main_sha": main_sha,
        "dry_run": bool(args.dry_run),
        "actions_taken": actions_taken,
        "unresolved_failures": unresolved,
        "mutation_or_incident": bool(actions_taken or unresolved),
        "checks": checks,
    }
    write_report(Path(args.output), payload)
    print(json.dumps({
        "actions_taken": actions_taken,
        "unresolved_failures": unresolved,
        "mutation_or_incident": payload["mutation_or_incident"],
    }))
    return 2 if unresolved else 0


if __name__ == "__main__":
    raise SystemExit(main())
