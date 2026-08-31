#!/usr/bin/env python3
"""Assemble and verify the compressed overnight swarm controller.

REVIEW STATUS: UNREVIEWED.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import tarfile
import tempfile
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload-dir", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    payload_dir = Path(args.payload_dir).resolve()
    manifest_path = Path(args.manifest).resolve()
    output = Path(args.output).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    parts = sorted(payload_dir.glob("controller.part-*"))
    expected_parts = manifest["payload"]["parts"]
    if [path.name for path in parts] != expected_parts:
        raise SystemExit(f"payload part closure mismatch: {[path.name for path in parts]}")

    encoded = b"".join(path.read_bytes() for path in parts)
    if sha256(encoded) != manifest["payload"]["base64_sha256"]:
        raise SystemExit("base64 payload digest mismatch")
    archive = base64.b64decode(encoded, validate=True)
    if sha256(archive) != manifest["payload"]["archive_sha256"]:
        raise SystemExit("controller archive digest mismatch")

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as temp:
        archive_path = Path(temp) / "controller.tar.gz"
        archive_path.write_bytes(archive)
        with tarfile.open(archive_path, "r:gz") as handle:
            members = handle.getmembers()
            expected_files = set(manifest["files"])
            actual_files = {member.name for member in members if member.isfile()}
            if actual_files != expected_files:
                raise SystemExit(f"archive file closure mismatch: {sorted(actual_files)}")
            for member in members:
                target = (output / member.name).resolve()
                if output not in target.parents:
                    raise SystemExit(f"unsafe archive member: {member.name}")
                if member.issym() or member.islnk():
                    raise SystemExit(f"links forbidden in controller archive: {member.name}")
            handle.extractall(output, filter="data")

    for name, expected in manifest["file_sha256"].items():
        data = (output / name).read_bytes()
        actual = sha256(data)
        if actual != expected:
            raise SystemExit(f"source digest mismatch for {name}: {actual}")
    print(json.dumps({"review_status": "UNREVIEWED", "assembled": sorted(manifest["files"]), "archive_sha256": sha256(archive)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
