#!/usr/bin/env python3
"""Record a bounded GPT provider attempt without manufacturing a review.

REVIEW STATUS: UNREVIEWED.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

LONDON = ZoneInfo("Europe/London")


def as_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered not in {"true", "false"}:
        raise argparse.ArgumentTypeError("expected true or false")
    return lowered == "true"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--sequence", required=True, type=int)
    parser.add_argument("--provider", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--inference-outcome", required=True)
    parser.add_argument("--created", required=True, type=as_bool)
    parser.add_argument("--reason", default="")
    args = parser.parse_args()

    if not 1 <= args.sequence <= 5:
        raise SystemExit("sequence must be between 1 and 5")

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    blocked = not args.created
    payload = {
        "schema": "chatgpt-audits.model-attempt.v1",
        "generation": "202608310322",
        "review_status": "UNREVIEWED",
        "classification": "observed",
        "sequence": args.sequence,
        "provider": args.provider,
        "model": args.model,
        "runtime": args.runtime,
        "inference_outcome": args.inference_outcome,
        "validated_review_created": args.created,
        "provider_blocked_or_response_rejected": blocked,
        "reason": args.reason or None,
        "checked_at": now.isoformat().replace("+00:00", "Z"),
        "checked_at_london": now.astimezone(LONDON).isoformat(),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
        "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "product_repository_writes": "FORBIDDEN",
        "product_workflow_dispatches": "FORBIDDEN",
    }
    (output / "MODEL-ATTEMPT.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )

    if blocked:
        (output / "PROVIDER-BLOCKED.md").write_text(
            "# GPT provider attempt not graduated\n\n"
            "> **REVIEW STATUS: UNREVIEWED**  \n"
            "> Classification: `observed`  \n\n"
            f"- Provider: `{args.provider}`\n"
            f"- Model: `{args.model}`\n"
            f"- Runtime: `{args.runtime}`\n"
            f"- Sequence requested: `{args.sequence}/5`\n"
            f"- Inference outcome: `{args.inference_outcome}`\n"
            f"- Reason: `{args.reason or 'not classified'}`\n\n"
            "No `MODEL-REVIEW.json` was created, so this attempt does not consume one "
            "of the five validated review slots. Inspect the workflow log for the exact "
            "Copilot policy, entitlement or response-contract error.\n",
            encoding="utf-8",
        )
    print(json.dumps({"created": args.created, "blocked": blocked, "reason": args.reason}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
