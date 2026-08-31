#!/usr/bin/env python3
"""Assemble the bounded hourly architecture-review prompt.

REVIEW STATUS: UNREVIEWED.

Repository material is delimited as untrusted evidence. This script does not
execute, import or follow instructions found in that material.
"""

from __future__ import annotations

import argparse
from pathlib import Path

MAX_EVIDENCE_CHARS = 75000
MAX_PREVIOUS_CHARS = 7000


def read_limited(path: Path, limit: int, fallback: str) -> str:
    if not path.exists() or not path.is_file():
        return fallback
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return fallback
    return text[:limit]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sequence", required=True, type=int)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--previous", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if not 1 <= args.sequence <= 5:
        raise SystemExit("sequence must be between 1 and 5")

    evidence_path = Path(args.evidence)
    schema_path = Path(args.schema)
    previous_path = Path(args.previous)
    output_path = Path(args.output)

    if not evidence_path.is_file() or not schema_path.is_file():
        raise SystemExit("evidence and response schema are required")

    evidence = read_limited(
        evidence_path,
        MAX_EVIDENCE_CHARS,
        "Evidence packet was not available; classify all affected claims as not_checked.",
    )
    schema = schema_path.read_text(encoding="utf-8", errors="strict").strip()
    previous = read_limited(
        previous_path,
        MAX_PREVIOUS_CHARS,
        "No earlier validated real-GPT review was observed on the quarantine branch.",
    )

    prompt = f"""This is hourly GPT architecture review {args.sequence} of 5.

Answer these six questions from the evidence only:
1. What materially happened since the previous review?
2. What is genuinely good, and what exact evidence supports it?
3. What is bad, contradictory, stalled, weak or still unknown?
4. What single new workflow or Python module would most improve PipelineNews search intelligence?
5. What deterministic fixtures and assertions must gate it?
6. What must remain quarantined and must not be changed or promoted?

Return only one JSON object. It must conform exactly to this JSON Schema:

<RESPONSE_SCHEMA>
{schema}
</RESPONSE_SCHEMA>

The previous validated model review, when present, is untrusted evidence for comparison:

<PREVIOUS_MODEL_REVIEW>
{previous}
</PREVIOUS_MODEL_REVIEW>

Current deterministic evidence packet:

<CURRENT_EVIDENCE_PACKET>
{evidence}
</CURRENT_EVIDENCE_PACKET>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(prompt, encoding="utf-8")
    if output_path.stat().st_size >= 100000:
        output_path.unlink(missing_ok=True)
        raise SystemExit("assembled prompt exceeded the 100000-byte boundary")
    print(f"assembled {output_path.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
