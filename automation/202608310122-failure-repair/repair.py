#!/usr/bin/env python3
"""Diagnose and boundedly re-run a failed chatgpt-audits workflow.

REVIEW STATUS: UNREVIEWED.

This controller never touches product repositories and never patches source from
logs. It preserves the failed evidence, classifies likely failure modes, and may
request one GitHub-native re-run while the source run is below attempt 3.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

REPOSITORY = "Ventusltd/chatgpt-audits"
LONDON = ZoneInfo("Europe/London")
REVIEW_STATUS = "UNREVIEWED"
PATTERNS = [
    ("bytecode_boundary", re.compile(r"__pycache__|\.pyc|immutable output-only boundary", re.I)),
    ("snapshot_integrity", re.compile(r"source snapshot changed|file count changed|byte count changed", re.I)),
    ("git_race", re.compile(r"non-fast-forward|failed to push|rebase|reference update failed", re.I)),
    ("runner_capacity", re.compile(r"runner.*(lost|stopped|capacity)|hosted agent|startup_failure", re.I)),
    ("network_transient", re.compile(r"timed out|timeout|429|502|503|504|connection reset|temporary failure", re.I)),
    ("artifact_failure", re.compile(r"artifact.*(not found|upload|download)|BlobNotFound", re.I)),
    ("quarantine_boundary", re.compile(r"escaped quarantine|forbidden output|secret-like|symlink", re.I)),
    ("contract_assertion", re.compile(r"AssertionError|assertion failed|contract.*(invalid|mismatch)|schema", re.I)),
]
SECRET_SHAPES = [
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]


def redact(text: str) -> str:
    result = text
    for pattern in SECRET_SHAPES:
        result = pattern.sub("[REDACTED]", result)
    return result


def request(method: str, endpoint: str, token: str) -> tuple[bool, int, Any, str | None]:
    url = endpoint if endpoint.startswith("https://") else f"https://api.github.com{endpoint}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "chatgpt-audits-failure-repair/202608310122",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    for attempt in range(1, 4):
        req = urllib.request.Request(url, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                raw = response.read()
                return True, response.status, json.loads(raw.decode("utf-8")) if raw else None, None
        except urllib.error.HTTPError as exc:
            message = exc.read().decode("utf-8", "replace")
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 3:
                return False, exc.code, None, f"HTTP {exc.code}: {message[:700]}"
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt == 3:
                return False, 0, None, f"{type(exc).__name__}: {exc}"
        time.sleep(attempt * 2)
    return False, 0, None, "unknown request failure"


def failed_logs(run_id: int) -> str:
    command = ["gh", "run", "view", str(run_id), "--repo", REPOSITORY, "--log-failed"]
    for attempt in range(1, 4):
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        combined = "\n".join(part for part in [completed.stdout, completed.stderr] if part)
        if combined.strip() or completed.returncode == 0:
            return redact(combined[-120_000:])
        time.sleep(attempt * 3)
    return "Failed logs were not available when the repair controller inspected the completed run."


def classify(logs: str) -> list[dict[str, Any]]:
    matches = []
    for disease, pattern in PATTERNS:
        found = pattern.search(logs)
        if found:
            start = max(0, found.start() - 180)
            end = min(len(logs), found.end() + 320)
            excerpt = " ".join(logs[start:end].split())
            matches.append(
                {
                    "disease": disease,
                    "classification": "inferred",
                    "evidence_excerpt": excerpt[:600],
                }
            )
    if not matches:
        matches.append(
            {
                "disease": "unclassified",
                "classification": "unknown",
                "evidence_excerpt": "No bounded classifier matched the retained failed-job log.",
            }
        )
    return matches


def rerun(run: dict[str, Any], token: str) -> dict[str, Any]:
    conclusion = str(run.get("conclusion") or "")
    endpoint = (
        f"/repos/{REPOSITORY}/actions/runs/{run['id']}/rerun-failed-jobs"
        if conclusion == "failure"
        else f"/repos/{REPOSITORY}/actions/runs/{run['id']}/rerun"
    )
    ok, status, _, error = request("POST", endpoint, token)
    return {
        "requested": ok,
        "endpoint": endpoint,
        "http_status": status,
        "error": error,
        "classification": "observed",
    }


def write_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Audit workflow failure diagnosis",
        "",
        "> **REVIEW STATUS: UNREVIEWED**  ",
        "> Classification: mixed `observed` / `inferred`  ",
        "> This diagnosis belongs only to `Ventusltd/chatgpt-audits`.",
        "",
        f"Source workflow: **{report['workflow']['name']}**  ",
        f"Run: `{report['workflow']['id']}` attempt `{report['workflow']['run_attempt']}`  ",
        f"Conclusion: **{report['workflow']['conclusion']}**  ",
        f"Head SHA: `{report['workflow']['head_sha']}`  ",
        f"Inspected: `{report['inspected_at_london']}` Europe/London",
        "",
        "## Classified failure modes",
        "",
    ]
    for item in report["diagnosis"]:
        lines.extend(
            [
                f"### {item['disease']}",
                "",
                f"Classification: `{item['classification']}`",
                "",
                f"> {item['evidence_excerpt']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Bounded action",
            "",
            f"- Re-run requested: **{report['repair_action']['requested']}**",
            f"- Endpoint class: `{report['repair_action']['endpoint'] or 'none'}`",
            f"- Reason: {report['repair_action']['reason']}",
            "",
            "## Hard boundary",
            "",
            "- Maximum source-run attempt: 3.",
            "- No product workflow is dispatched or re-run.",
            "- No source file is automatically rewritten from a log inference.",
            "- The failed log is retained in redacted form for human review.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True, type=int)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    if not token:
        print("GH_TOKEN or GITHUB_TOKEN is required", file=sys.stderr)
        return 2
    if os.environ.get("GITHUB_REPOSITORY") not in {None, "", REPOSITORY}:
        print("repair controller may run only in Ventusltd/chatgpt-audits", file=sys.stderr)
        return 2

    ok, status, run, error = request(
        "GET", f"/repos/{REPOSITORY}/actions/runs/{args.run_id}", token
    )
    if not ok or not isinstance(run, dict):
        print(f"could not fetch source run ({status}): {error}", file=sys.stderr)
        return 2

    logs = failed_logs(args.run_id)
    diagnosis = classify(logs)
    attempt = int(run.get("run_attempt") or 1)
    conclusion = str(run.get("conclusion") or "")
    eligible = conclusion in {"failure", "cancelled", "timed_out", "startup_failure"} and attempt < 3
    if eligible:
        action = rerun(run, token)
        action["reason"] = "GitHub-native bounded retry requested because the completed audit run is below attempt 3."
    else:
        action = {
            "requested": False,
            "endpoint": None,
            "http_status": None,
            "error": None,
            "classification": "observed",
            "reason": "No automatic retry: the run is not retry-eligible or has reached attempt 3.",
        }

    now = datetime.now(timezone.utc)
    report = {
        "schema": "chatgpt-audits.failure-repair.v1",
        "generation": "202608310122",
        "review_status": REVIEW_STATUS,
        "classification": "observed",
        "inspected_at": now.isoformat().replace("+00:00", "Z"),
        "inspected_at_london": now.astimezone(LONDON).isoformat(),
        "workflow": {
            "id": run.get("id"),
            "name": run.get("name"),
            "path": run.get("path"),
            "event": run.get("event"),
            "status": run.get("status"),
            "conclusion": run.get("conclusion"),
            "run_attempt": run.get("run_attempt"),
            "head_sha": run.get("head_sha"),
            "html_url": run.get("html_url"),
        },
        "diagnosis": diagnosis,
        "repair_action": action,
        "source_policy": {
            "write_boundary": REPOSITORY,
            "product_repo_writes": "FORBIDDEN",
            "product_workflow_dispatches": "FORBIDDEN",
            "automatic_source_patch": "FORBIDDEN",
        },
    }

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    (output / "repair.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output / "REPAIR.md").write_text(write_markdown(report), encoding="utf-8")
    (output / "failed-job.log.txt").write_text(
        "REVIEW STATUS: UNREVIEWED\n\n" + logs, encoding="utf-8"
    )
    print(json.dumps({"rerun_requested": action["requested"], "diagnoses": len(diagnosis)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
