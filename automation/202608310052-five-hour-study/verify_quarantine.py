#!/usr/bin/env python3
"""Verify the five-hour study remained inside its quarantine boundary.

REVIEW STATUS: UNREVIEWED.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Iterator, Sequence

REVIEW_STATUS = "UNREVIEWED"
SKIP_DIRS = {
    ".git",
    ".idea",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "vendor",
}
FORBIDDEN_OUTPUT_DIRS = {
    ".git",
    ".idea",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "vendor",
}
SECRET_PATTERNS = {
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "github_pat": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
ALLOWED_JSON_CLASSIFICATIONS = {
    "observed",
    "inferred",
    "contradicted",
    "unknown",
    "not_checked",
    "not_observed_in_snapshot",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_files(root: Path) -> Iterator[Path]:
    if not root.exists():
        return
    for directory, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS)
        base = Path(directory)
        for name in sorted(filenames):
            path = base / name
            if path.is_file() and not path.is_symlink():
                yield path


def tree_digest(root: Path) -> tuple[str, int, int]:
    digest = hashlib.sha256()
    count = 0
    total = 0
    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        size = path.stat().st_size
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(str(size).encode())
        digest.update(b"\0")
        digest.update(sha256_file(path).encode())
        digest.update(b"\n")
        count += 1
        total += size
    return digest.hexdigest(), count, total


def parse_status_paths(raw: bytes) -> list[str]:
    paths: list[str] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        text = item.decode("utf-8", errors="replace")
        paths.append(text[3:] if len(text) >= 4 else text)
    return paths


def git_changed_paths(audit_root: Path) -> list[str]:
    import subprocess

    completed = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=audit_root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.decode("utf-8", errors="replace"))
    return parse_status_paths(completed.stdout)


def ensure_unreviewed_label(path: Path) -> list[str]:
    failures: list[str] = []
    suffix = path.suffix.lower()
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return failures
    if suffix in {".md", ".txt"}:
        if REVIEW_STATUS not in "\n".join(text.splitlines()[:12]):
            failures.append(f"missing UNREVIEWED label near top: {path}")
    elif suffix == ".json":
        try:
            payload: Any = json.loads(text)
        except json.JSONDecodeError as exc:
            failures.append(f"invalid JSON {path}: {exc}")
            return failures
        if not isinstance(payload, dict) or payload.get("review_status") != REVIEW_STATUS:
            failures.append(f"JSON missing review_status=UNREVIEWED: {path}")
        classification = payload.get("classification") if isinstance(payload, dict) else None
        if classification is not None and classification not in ALLOWED_JSON_CLASSIFICATIONS:
            failures.append(f"invalid top-level classification {classification!r}: {path}")
    elif suffix in {".py", ".js", ".mjs", ".cjs", ".ts"}:
        if REVIEW_STATUS not in "\n".join(text.splitlines()[:8]):
            failures.append(f"reference code missing UNREVIEWED label: {path}")
    return failures


def verify(args: argparse.Namespace) -> int:
    audit_root = Path(args.audit_root).resolve()
    output_root = Path(args.output_root).resolve()
    source_root = Path(args.source_root).resolve()
    manifest_path = Path(args.manifest).resolve()
    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    failures: list[str] = []
    try:
        output_rel = output_root.relative_to(audit_root).as_posix()
    except ValueError:
        failures.append("output root is outside audit checkout")
        output_rel = ""

    expected_prefix = "202608310033-study/AUTOMATION-RUNS/"
    if not output_rel.startswith(expected_prefix):
        failures.append(f"output root must start with {expected_prefix}: {output_rel}")

    if output_root.is_symlink() or not output_root.is_dir():
        failures.append("output root is missing, not a directory or is a symlink")

    changed = git_changed_paths(audit_root)
    for path in changed:
        normalised = path.replace("\\", "/")
        if not (normalised == output_rel or normalised.startswith(output_rel + "/")):
            failures.append(f"changed path escaped quarantine: {normalised}")

    max_file = int(plan["limits"]["max_output_file_bytes"])
    max_total = int(plan["limits"]["max_total_output_bytes"])
    total_bytes = 0
    for directory, dirnames, filenames in os.walk(output_root):
        for dirname in dirnames:
            if dirname in FORBIDDEN_OUTPUT_DIRS:
                failures.append(f"forbidden generated directory in output: {Path(directory) / dirname}")
        for filename in filenames:
            if filename.endswith((".pyc", ".pyo")):
                failures.append(f"compiled bytecode forbidden in output: {Path(directory) / filename}")

    for path in iter_files(output_root):
        if path.is_symlink():
            failures.append(f"symlink forbidden in output: {path}")
            continue
        size = path.stat().st_size
        total_bytes += size
        if size > max_file:
            failures.append(f"output file exceeds {max_file} bytes: {path} ({size})")
        failures.extend(ensure_unreviewed_label(path))
        if size <= max_file:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                failures.append(f"binary output forbidden: {path}")
                continue
            for name, pattern in SECRET_PATTERNS.items():
                if pattern.search(text):
                    failures.append(f"possible {name} in output: {path}")
    if total_bytes > max_total:
        failures.append(f"total output exceeds {max_total} bytes: {total_bytes}")

    for entry in manifest.get("repositories", []):
        if entry.get("status") != "SNAPSHOT_READY":
            continue
        name = str(entry["name"])
        repo_root = source_root / name
        if not repo_root.exists():
            failures.append(f"source snapshot disappeared: {name}")
            continue
        if (repo_root / ".git").exists():
            failures.append(f"source git metadata was not removed: {name}")
        digest, files, total = tree_digest(repo_root)
        if digest != entry.get("snapshot_tree_sha256"):
            failures.append(
                f"source snapshot changed: {name} expected={entry.get('snapshot_tree_sha256')} actual={digest}"
            )
        if files != int(entry.get("snapshot_files", -1)):
            failures.append(f"source file count changed: {name} expected={entry.get('snapshot_files')} actual={files}")
        if total != int(entry.get("snapshot_bytes", -1)):
            failures.append(f"source byte count changed: {name} expected={entry.get('snapshot_bytes')} actual={total}")

    required_files = ["README.md", "RUN-CONTEXT.json", "SOURCE-SNAPSHOT.json"]
    phase = int(args.phase)
    phase_requirements = {
        1: ["01-REPOSITORY-INVENTORY.md", "01-REPOSITORY-INVENTORY.json", "checkpoint-01.json"],
        2: ["02-PIPELINENEWS-ENGINE-AUDIT.md", "02-PIPELINENEWS-ENGINE-AUDIT.json", "checkpoint-02.json"],
        3: ["03-FUNDING-AND-PROCUREMENT-SIGNALS.md", "03-EVENT-CONTRACT-CANDIDATE.json", "checkpoint-03.json"],
        4: ["04-SEAMS-AND-CLAUDE-CROSSCHECK.md", "04-CLAUDE-CROSSCHECK-LEDGER.json", "checkpoint-04.json"],
        5: [
            "05-PIPELINENEWS-VNEXT.md",
            "checkpoint-05.json",
            "next-versions/202608310052-pipelinenews-intelligence-vnext/README.md",
            "next-versions/202608310052-pipelinenews-intelligence-vnext/reference/state_machine.py",
            "next-versions/202608310052-pipelinenews-intelligence-vnext/reference/test_state_machine.py"
        ],
        6: ["00-EXECUTIVE-SYNTHESIS.md", "REVIEW-QUEUE.md", "RUN-MANIFEST.json"]
    }
    for current in range(1, min(phase, 5) + 1):
        required_files.extend(phase_requirements[current])
    if phase == 6:
        for current in range(1, 6):
            required_files.extend(phase_requirements[current])
        required_files.extend(phase_requirements[6])
    for rel in required_files:
        if not (output_root / rel).is_file():
            failures.append(f"required output missing for phase {phase}: {rel}")

    if failures:
        print("QUARANTINE VERIFICATION FAILED", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "status": "PASS",
                "phase": phase,
                "output_root": output_rel,
                "changed_paths": changed,
                "total_output_bytes": total_bytes,
                "source_snapshots_verified": sum(1 for item in manifest.get("repositories", []) if item.get("status") == "SNAPSHOT_READY")
            },
            indent=2
        )
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--phase", required=True, type=int, choices=range(1, 7))
    args = parser.parse_args(argv)
    try:
        return verify(args)
    except Exception as exc:
        print(f"QUARANTINE VERIFICATION ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
