#!/usr/bin/env python3
"""Validate and render a structured GitHub Models GPT response.

REVIEW STATUS: UNREVIEWED.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

REVIEW_STATUS = "UNREVIEWED"
LONDON = ZoneInfo("Europe/London")
CLASSIFICATIONS = {
    "observed",
    "inferred",
    "contradicted",
    "unknown",
    "not_checked",
    "not_observed_in_snapshot",
}
REQUIRED_KEYS = {
    "overall_assessment",
    "what_happened",
    "good",
    "bad",
    "recommended_improvement",
    "deterministic_tests",
    "do_not_change",
    "uncertainties",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_response(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    text = raw.decode("utf-8", "replace").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise ValueError("model response must be a JSON object")
    return payload, raw


def require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def require_string_list(value: Any, field: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    result = [require_string(item, f"{field}[]") for item in value]
    return result


def validate_claim_rows(value: Any, field: str, issue_mode: bool = False) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise ValueError(f"{field} must be an array")
    rows: list[dict[str, str]] = []
    for index, row in enumerate(value):
        if not isinstance(row, dict):
            raise ValueError(f"{field}[{index}] must be an object")
        statement_key = "issue" if issue_mode else "claim"
        classification = require_string(row.get("classification"), f"{field}[{index}].classification")
        if classification not in CLASSIFICATIONS:
            raise ValueError(f"unsupported classification {classification!r}")
        item = {
            statement_key: require_string(row.get(statement_key), f"{field}[{index}].{statement_key}"),
            "evidence": require_string(row.get("evidence"), f"{field}[{index}].evidence"),
            "classification": classification,
        }
        if issue_mode:
            item["impact"] = require_string(row.get("impact"), f"{field}[{index}].impact")
        rows.append(item)
    return rows


def validate_improvement(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("recommended_improvement must be an object")
    kind = require_string(value.get("kind"), "recommended_improvement.kind")
    if kind not in {"workflow", "python"}:
        raise ValueError("recommended_improvement.kind must be workflow or python")
    return {
        "kind": kind,
        "name": require_string(value.get("name"), "recommended_improvement.name"),
        "purpose": require_string(value.get("purpose"), "recommended_improvement.purpose"),
        "evidence_basis": require_string(
            value.get("evidence_basis"), "recommended_improvement.evidence_basis"
        ),
        "algorithm": require_string(value.get("algorithm"), "recommended_improvement.algorithm"),
        "inputs": require_string_list(value.get("inputs"), "recommended_improvement.inputs"),
        "outputs": require_string_list(value.get("outputs"), "recommended_improvement.outputs"),
        "rejection_conditions": require_string_list(
            value.get("rejection_conditions"), "recommended_improvement.rejection_conditions"
        ),
    }


def validate_tests(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or not value:
        raise ValueError("deterministic_tests must be a non-empty array")
    result = []
    for index, row in enumerate(value):
        if not isinstance(row, dict):
            raise ValueError(f"deterministic_tests[{index}] must be an object")
        result.append(
            {
                "name": require_string(row.get("name"), f"deterministic_tests[{index}].name"),
                "fixture": require_string(row.get("fixture"), f"deterministic_tests[{index}].fixture"),
                "assertion": require_string(
                    row.get("assertion"), f"deterministic_tests[{index}].assertion"
                ),
            }
        )
    return result


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    missing = REQUIRED_KEYS - payload.keys()
    extra = payload.keys() - REQUIRED_KEYS
    if missing:
        raise ValueError(f"missing required response keys: {sorted(missing)}")
    if extra:
        raise ValueError(f"unexpected response keys: {sorted(extra)}")
    return {
        "overall_assessment": require_string(payload["overall_assessment"], "overall_assessment"),
        "what_happened": validate_claim_rows(payload["what_happened"], "what_happened"),
        "good": validate_claim_rows(payload["good"], "good"),
        "bad": validate_claim_rows(payload["bad"], "bad", issue_mode=True),
        "recommended_improvement": validate_improvement(payload["recommended_improvement"]),
        "deterministic_tests": validate_tests(payload["deterministic_tests"]),
        "do_not_change": require_string_list(payload["do_not_change"], "do_not_change"),
        "uncertainties": require_string_list(payload["uncertainties"], "uncertainties"),
    }


def bullet_claim(row: dict[str, str], issue_mode: bool = False) -> str:
    key = "issue" if issue_mode else "claim"
    suffix = f" Impact: {row['impact']}" if issue_mode else ""
    return (
        f"- **{row[key]}** — `{row['classification']}`. "
        f"Evidence: {row['evidence']}.{suffix}"
    )


def render_markdown(payload: dict[str, Any], sequence: int, model: str) -> str:
    improvement = payload["recommended_improvement"]
    lines = [
        "# GPT hourly architecture review",
        "",
        f"> **REVIEW STATUS: {REVIEW_STATUS}**  ",
        "> Model reasoning is advisory and quarantined. Source excerpts were supplied as untrusted evidence.  ",
        "> Nothing in this review is installed, promoted or published to a product repository.",
        "",
        f"Sequence: **{sequence}/5**  ",
        f"Model: `{model}`",
        "",
        "## Overall assessment",
        "",
        payload["overall_assessment"],
        "",
        "## What happened",
        "",
    ]
    lines.extend(bullet_claim(row) for row in payload["what_happened"])
    lines.extend(["", "## What is good", ""])
    lines.extend(bullet_claim(row) for row in payload["good"])
    lines.extend(["", "## What is bad, contradictory or unknown", ""])
    lines.extend(bullet_claim(row, issue_mode=True) for row in payload["bad"])
    lines.extend(
        [
            "",
            "## Highest-leverage quarantined improvement",
            "",
            f"- Type: `{improvement['kind']}`",
            f"- Name: `{improvement['name']}`",
            f"- Purpose: {improvement['purpose']}",
            f"- Evidence basis: {improvement['evidence_basis']}",
            "",
            "### Algorithm",
            "",
            improvement["algorithm"],
            "",
            "### Inputs",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in improvement["inputs"])
    lines.extend(["", "### Outputs", ""])
    lines.extend(f"- {item}" for item in improvement["outputs"])
    lines.extend(["", "### Rejection conditions", ""])
    lines.extend(f"- {item}" for item in improvement["rejection_conditions"])
    lines.extend(["", "## Deterministic acceptance tests", ""])
    for test in payload["deterministic_tests"]:
        lines.extend(
            [
                f"### {test['name']}",
                "",
                f"- Fixture: {test['fixture']}",
                f"- Assertion: {test['assertion']}",
                "",
            ]
        )
    lines.extend(["## Do not change or promote", ""])
    lines.extend(f"- {item}" for item in payload["do_not_change"])
    lines.extend(["", "## Remaining uncertainties", ""])
    lines.extend(f"- {item}" for item in payload["uncertainties"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--response", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--sequence", required=True, type=int)
    parser.add_argument("--model", required=True)
    args = parser.parse_args()
    if not 1 <= args.sequence <= 5:
        raise SystemExit("sequence must be between 1 and 5")

    response_path = Path(args.response)
    prompt_path = Path(args.prompt)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    parsed, raw = load_response(response_path)
    validated = validate(parsed)
    prompt_raw = prompt_path.read_bytes()
    now = datetime.now(timezone.utc)

    (output / "MODEL-RAW.txt").write_bytes(raw)
    (output / "MODEL-REVIEW.json").write_text(
        json.dumps(validated, indent=2) + "\n", encoding="utf-8"
    )
    (output / "MODEL-REVIEW.md").write_text(
        render_markdown(validated, args.sequence, args.model), encoding="utf-8"
    )
    metadata = {
        "schema": "chatgpt-audits.real-gpt-review-metadata.v1",
        "generation": "202608310322",
        "review_status": REVIEW_STATUS,
        "classification": "inferred",
        "sequence": args.sequence,
        "model": args.model,
        "github_models_action_sha": "b81b2afb8390ee6839b494a404766bef6493c7d9",
        "created_at": now.isoformat().replace("+00:00", "Z"),
        "created_at_london": now.astimezone(LONDON).isoformat(),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
        "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "prompt_sha256": sha256_bytes(prompt_raw),
        "raw_response_sha256": sha256_bytes(raw),
        "product_repository_writes": "FORBIDDEN",
        "product_workflow_dispatches": "FORBIDDEN",
    }
    (output / "MODEL-METADATA.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"sequence": args.sequence, "model": args.model, "validated": True}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
