#!/usr/bin/env python3
"""Deterministic local tests for the GPT reasoning timer controller.

REVIEW STATUS: UNREVIEWED.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_RUNTIME_SHA = "37fa67686a9e4ed8d46dcd6a9c80ab524dea840ecaa0a3f7edf8d09f961b97a9"
EXPECTED_KEYS = {
    "overall_assessment",
    "what_happened",
    "good",
    "bad",
    "recommended_improvement",
    "deterministic_tests",
    "do_not_change",
    "uncertainties",
}


def run(command: list[str], expected: int = 0) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    if completed.returncode != expected:
        raise RuntimeError(
            f"command returned {completed.returncode}, expected {expected}: {' '.join(command)}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


def valid_payload() -> dict[str, object]:
    return {
        "overall_assessment": "Synthetic renderer self-test.",
        "what_happened": [
            {
                "claim": "A test ran.",
                "evidence": "Synthetic fixture.",
                "classification": "observed",
            }
        ],
        "good": [
            {
                "claim": "The fixture is bounded.",
                "evidence": "Local temporary files only.",
                "classification": "observed",
            }
        ],
        "bad": [
            {
                "issue": "This is not production evidence.",
                "evidence": "The payload is synthetic.",
                "classification": "observed",
                "impact": "It cannot support a product claim.",
            }
        ],
        "recommended_improvement": {
            "kind": "python",
            "name": "synthetic_test.py",
            "purpose": "Exercise the renderer.",
            "evidence_basis": "Local fixture.",
            "algorithm": "Parse and validate strict fields.",
            "inputs": ["Synthetic JSON"],
            "outputs": ["Rendered Markdown"],
            "rejection_conditions": ["Missing required field"],
        },
        "deterministic_tests": [
            {"name": "parse", "fixture": "Valid JSON", "assertion": "Exit zero"},
            {"name": "schema", "fixture": "Missing key", "assertion": "Reject"},
            {"name": "boundary", "fixture": "Temporary output", "assertion": "No product path"},
        ],
        "do_not_change": ["Product repositories"],
        "uncertainties": ["None relevant to this synthetic fixture"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--renderer", required=True)
    parser.add_argument("--assembler", required=True)
    parser.add_argument("--recorder", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--runtime-source", required=True)
    args = parser.parse_args()

    renderer = Path(args.renderer)
    assembler = Path(args.assembler)
    recorder = Path(args.recorder)
    schema_path = Path(args.schema)
    runtime_path = Path(args.runtime_source)
    for path in (renderer, assembler, recorder, schema_path, runtime_path):
        if not path.is_file():
            raise SystemExit(f"missing controller input: {path}")

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
        raise SystemExit("response schema is not strict at the root")
    if set(schema.get("required", [])) != EXPECTED_KEYS:
        raise SystemExit("response schema required keys changed")

    source = json.loads(runtime_path.read_text(encoding="utf-8"))
    if source.get("version") != "1.0.82" or source.get("sha256") != EXPECTED_RUNTIME_SHA:
        raise SystemExit("Copilot runtime source card changed without updating tests")
    if source.get("network_classification") != "SUPERVISED_SOURCE_CARDED_RUNTIME_FETCH":
        raise SystemExit("Copilot runtime fetch is not source-carded")

    with tempfile.TemporaryDirectory(prefix="chatgpt-audits-gpt-timer-") as temporary:
        root = Path(temporary)
        response = root / "response.json"
        prompt = root / "prompt.txt"
        evidence = root / "evidence.md"
        previous = root / "previous.md"
        assembled = root / "assembled.txt"
        rendered = root / "rendered"

        response.write_text(json.dumps(valid_payload()), encoding="utf-8")
        prompt.write_text("synthetic prompt\n", encoding="utf-8")
        evidence.write_text("synthetic evidence\n", encoding="utf-8")
        previous.write_text("synthetic previous review\n", encoding="utf-8")

        run(
            [
                sys.executable,
                str(assembler),
                "--sequence",
                "1",
                "--evidence",
                str(evidence),
                "--schema",
                str(schema_path),
                "--previous",
                str(previous),
                "--output",
                str(assembled),
            ]
        )
        assembled_text = assembled.read_text(encoding="utf-8")
        if "<CURRENT_EVIDENCE_PACKET>" not in assembled_text or "synthetic evidence" not in assembled_text:
            raise SystemExit("assembler omitted bounded evidence delimiters")

        run(
            [
                sys.executable,
                str(renderer),
                "--response",
                str(response),
                "--prompt",
                str(prompt),
                "--output",
                str(rendered),
                "--sequence",
                "1",
                "--model",
                "gpt-5",
                "--provider",
                "github-copilot-cli",
                "--runtime",
                "copilot-cli/1.0.82",
            ]
        )
        for name in ("MODEL-REVIEW.md", "MODEL-REVIEW.json", "MODEL-METADATA.json"):
            if not (rendered / name).is_file():
                raise SystemExit(f"renderer did not create {name}")

        invalid = valid_payload()
        invalid.pop("bad")
        response.write_text(json.dumps(invalid), encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                str(renderer),
                "--response",
                str(response),
                "--prompt",
                str(prompt),
                "--output",
                str(root / "invalid"),
                "--sequence",
                "1",
                "--model",
                "gpt-5",
                "--provider",
                "github-copilot-cli",
                "--runtime",
                "copilot-cli/1.0.82",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode == 0:
            raise SystemExit("renderer accepted an invalid response missing a required key")

        run(
            [
                sys.executable,
                str(recorder),
                "--output",
                str(root / "blocked"),
                "--sequence",
                "1",
                "--provider",
                "github-copilot-cli",
                "--model",
                "gpt-5",
                "--runtime",
                "copilot-cli/1.0.82",
                "--inference-outcome",
                "failure",
                "--created",
                "false",
                "--reason",
                "SYNTHETIC_BLOCK",
            ]
        )
        if (root / "blocked" / "MODEL-REVIEW.json").exists():
            raise SystemExit("blocked provider attempt manufactured a validated review")
        if not (root / "blocked" / "PROVIDER-BLOCKED.md").is_file():
            raise SystemExit("blocked provider attempt was not retained")

    print("all deterministic GPT timer self-tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
