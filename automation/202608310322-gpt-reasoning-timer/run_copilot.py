#!/usr/bin/env python3
"""Run one bounded GitHub Copilot GPT judgement and retain exact diagnostics.

REVIEW STATUS: UNREVIEWED.

The CLI runs in an empty temporary directory with a fresh configuration home.
All model tools except `ask_user` are unavailable, `--no-ask-user` is enabled,
and explicit deny rules cover reads, writes, shell commands, URLs and memory.
The model therefore receives only the assembled prompt and cannot inspect or
mutate a product repository.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping
from zoneinfo import ZoneInfo

LONDON = ZoneInfo("Europe/London")
REVIEW_STATUS = "UNREVIEWED"
MINIMUM_AI_CREDITS = 30
TOKEN_PATTERNS = [
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._~-]{20,}", re.I),
]


def redact(text: str, secrets: list[str]) -> str:
    result = text
    for secret in sorted((item for item in secrets if item), key=len, reverse=True):
        result = result.replace(secret, "[REDACTED]")
    for pattern in TOKEN_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


def classify(exit_code: int, stderr: str, stdout: str) -> str:
    if exit_code == 0 and stdout.strip():
        return "SUCCESS"
    text = f"{stderr}\n{stdout}".lower()
    if "allow use of copilot cli billed to the organization" in text:
        return "ORG_COPILOT_BILLING_POLICY_DISABLED"
    if "copilot cli" in text and "policy" in text and any(
        marker in text for marker in ("disabled", "not enabled", "blocked", "denied")
    ):
        return "ORG_COPILOT_POLICY_BLOCKED"
    if any(marker in text for marker in ("401", "403", "unauthorized", "forbidden")):
        return "COPILOT_AUTH_OR_ENTITLEMENT_REJECTED"
    if "model" in text and any(
        marker in text
        for marker in ("not found", "not available", "unsupported", "invalid model", "unknown model")
    ):
        return "REQUESTED_GPT_MODEL_UNAVAILABLE"
    if any(marker in text for marker in ("trust this", "permission prompt", "requires approval")):
        return "NONINTERACTIVE_PERMISSION_REJECTED"
    if "rate limit" in text or "quota" in text or "budget" in text:
        return "COPILOT_QUOTA_OR_BUDGET_REJECTED"
    if exit_code == 124:
        return "COPILOT_TIMEOUT"
    if exit_code == 0:
        return "EMPTY_MODEL_RESPONSE"
    return f"COPILOT_CLI_EXIT_{exit_code}"


def minimal_environment(token: str, home: Path) -> dict[str, str]:
    env = {
        "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
        "HOME": str(home),
        "COPILOT_HOME": str(home / ".copilot"),
        "GITHUB_TOKEN": token,
        "CI": "true",
        "TERM": "dumb",
        "NO_COLOR": "1",
        "COPILOT_AUTO_UPDATE": "false",
        "COPILOT_ENABLE_HTTP2": "false",
    }
    for key in (
        "SSL_CERT_FILE",
        "SSL_CERT_DIR",
        "HTTPS_PROXY",
        "HTTP_PROXY",
        "ALL_PROXY",
        "NO_PROXY",
        "https_proxy",
        "http_proxy",
        "all_proxy",
        "no_proxy",
    ):
        value = os.environ.get(key)
        if value:
            env[key] = value
    return env


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--system", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=240)
    args = parser.parse_args()

    cli = Path(args.cli).resolve()
    prompt_path = Path(args.prompt).resolve()
    system_path = Path(args.system).resolve()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)

    if not cli.is_file() or not os.access(cli, os.X_OK):
        raise SystemExit(f"Copilot CLI is not executable: {cli}")
    if not prompt_path.is_file() or not system_path.is_file():
        raise SystemExit("prompt and system instruction files are required")

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")

    system = system_path.read_text(encoding="utf-8", errors="strict").strip()
    prompt = prompt_path.read_text(encoding="utf-8", errors="replace").strip()
    combined = (
        f"<SYSTEM_BOUNDARY>\n{system}\n</SYSTEM_BOUNDARY>\n\n"
        f"<USER_EVIDENCE_REQUEST>\n{prompt}\n</USER_EVIDENCE_REQUEST>"
    )
    if len(combined.encode("utf-8")) >= 100_000:
        raise SystemExit("combined Copilot prompt exceeded 100000 bytes")

    runtime = output / "copilot-isolated-runtime"
    work = runtime / "empty-workspace"
    home = runtime / "home"
    logs = runtime / "logs"
    for path in (work, home, logs):
        path.mkdir(parents=True, exist_ok=True)

    command = [
        str(cli),
        "-C",
        str(work),
        "-p",
        combined,
        "-s",
        "--no-ask-user",
        "--no-banner",
        "--model",
        args.model,
        "--max-ai-credits",
        str(MINIMUM_AI_CREDITS),
        "--yolo",
        "--available-tools=ask_user",
        "--deny-tool=read",
        "--deny-tool=write",
        "--deny-tool=shell",
        "--deny-tool=url",
        "--deny-tool=memory",
        "--log-level=debug",
        "--log-dir",
        str(logs),
    ]
    env = minimal_environment(token, home)
    started = datetime.now(timezone.utc)
    try:
        completed = subprocess.run(
            command,
            cwd=work,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=max(30, args.timeout_seconds),
            check=False,
        )
        exit_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as exc:
        exit_code = 124
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        stderr += f"\nTimed out after {args.timeout_seconds} seconds."

    finished = datetime.now(timezone.utc)
    secrets = [token, os.environ.get("COPILOT_GITHUB_TOKEN", ""), os.environ.get("GH_TOKEN", "")]
    clean_stdout = redact(stdout, secrets)
    clean_stderr = redact(stderr, secrets)
    classification = classify(exit_code, clean_stderr, clean_stdout)

    (output / "COPILOT-STDOUT.txt").write_text(clean_stdout, encoding="utf-8")
    (output / "COPILOT-STDERR.txt").write_text(clean_stderr, encoding="utf-8")
    (output / "COPILOT-RESPONSE.txt").write_text(clean_stdout, encoding="utf-8")
    command_record = [
        "copilot",
        "-C",
        "<EMPTY_WORKSPACE>",
        "-p",
        "<ASSEMBLED_PROMPT>",
        "-s",
        "--no-ask-user",
        "--no-banner",
        "--model",
        args.model,
        "--max-ai-credits",
        str(MINIMUM_AI_CREDITS),
        "--yolo",
        "--available-tools=ask_user",
        "--deny-tool=read",
        "--deny-tool=write",
        "--deny-tool=shell",
        "--deny-tool=url",
        "--deny-tool=memory",
    ]
    report: Mapping[str, object] = {
        "schema": "chatgpt-audits.direct-copilot-run.v2",
        "generation": "202608310414",
        "review_status": REVIEW_STATUS,
        "classification": "observed",
        "provider": "github-copilot-cli",
        "model": args.model,
        "exit_code": exit_code,
        "outcome": "success" if classification == "SUCCESS" else "failure",
        "reason": classification,
        "stdout_bytes": len(clean_stdout.encode("utf-8")),
        "stderr_bytes": len(clean_stderr.encode("utf-8")),
        "started_at": started.isoformat().replace("+00:00", "Z"),
        "finished_at": finished.isoformat().replace("+00:00", "Z"),
        "finished_at_london": finished.astimezone(LONDON).isoformat(),
        "isolated_empty_workspace": True,
        "fresh_copilot_home": True,
        "model_tools_available": ["ask_user"],
        "ask_user_disabled": True,
        "explicit_denials": ["read", "write", "shell", "url", "memory"],
        "max_ai_credits": MINIMUM_AI_CREDITS,
        "command": command_record,
        "product_repository_writes": "FORBIDDEN",
        "product_workflow_dispatches": "FORBIDDEN",
    }
    (output / "COPILOT-RUN.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"outcome": report["outcome"], "reason": classification, "exit_code": exit_code}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
