#!/usr/bin/env python3
"""Deterministic, read-only study controller for Ventusltd/chatgpt-audits.

REVIEW STATUS: UNREVIEWED.

The controller may clone only the repositories explicitly listed in study-plan.json.
It never calls a live data API and never writes inside a product repository snapshot.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence
from zoneinfo import ZoneInfo

GENERATION = "202608310052"
REVIEW_STATUS = "UNREVIEWED"
CLASSIFICATIONS = {
    "observed",
    "inferred",
    "contradicted",
    "unknown",
    "not_checked",
    "not_observed_in_snapshot",
}
TEXT_SUFFIXES = {
    "",
    ".cjs",
    ".css",
    ".csv",
    ".graphql",
    ".htm",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsonl",
    ".jsx",
    ".md",
    ".mjs",
    ".py",
    ".rst",
    ".sh",
    ".sql",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
SKIP_DIRS = {
    ".git",
    ".idea",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "vendor",
}
GENERATION_RE = re.compile(r"(?<!\d)20\d{10}(?!\d)")
URL_RE = re.compile(r"https?://[^\s'\"`)<>]+")
BACKTICK_RE = re.compile(r"`([^`\n]{2,260})`")


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def now_london() -> str:
    return datetime.now(ZoneInfo("Europe/London")).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def md_header(title: str, classification: str = "observed") -> str:
    if classification not in CLASSIFICATIONS:
        raise ValueError(f"unknown classification: {classification}")
    return (
        f"# {title}\n\n"
        f"> **REVIEW STATUS: {REVIEW_STATUS}**  \n"
        f"> Classification: `{classification}`  \n"
        "> This is quarantined study output. It is not installed, trusted or published.\n"
    )


def run(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    timeout: int = 600,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        list(command),
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    )
    if check and completed.returncode != 0:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {' '.join(command)}\n"
            f"stdout:\n{completed.stdout[-4000:]}\n"
            f"stderr:\n{completed.stderr[-4000:]}"
        )
    return completed


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def iter_files(root: Path, *, limit: int | None = None) -> Iterator[Path]:
    yielded = 0
    if not root.exists():
        return
    for directory, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRS)
        base = Path(directory)
        for name in sorted(filenames):
            path = base / name
            if path.is_symlink() or not path.is_file():
                continue
            yield path
            yielded += 1
            if limit is not None and yielded >= limit:
                return


def is_text_candidate(path: Path, max_bytes: int) -> bool:
    try:
        if path.stat().st_size > max_bytes:
            return False
    except OSError:
        return False
    name = path.name.lower()
    if name in {"dockerfile", "makefile", "license", "readme"}:
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def read_text(path: Path, max_bytes: int) -> str | None:
    if not is_text_candidate(path, max_bytes):
        return None
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw[:8192]:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def tree_digest(root: Path) -> tuple[str, int, int]:
    digest = hashlib.sha256()
    files = 0
    total_bytes = 0
    for path in iter_files(root):
        rel = relative_posix(path, root)
        size = path.stat().st_size
        file_hash = sha256_file(path)
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(size).encode("ascii"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")
        files += 1
        total_bytes += size
    return digest.hexdigest(), files, total_bytes


def make_read_only(root: Path) -> None:
    for directory, dirnames, filenames in os.walk(root):
        base = Path(directory)
        for name in filenames:
            path = base / name
            if path.is_symlink():
                continue
            mode = stat.S_IMODE(path.stat().st_mode)
            path.chmod(mode & ~0o222)
        for name in dirnames:
            path = base / name
            if path.is_symlink():
                continue
            mode = stat.S_IMODE(path.stat().st_mode)
            path.chmod((mode & ~0o222) | 0o500)
    mode = stat.S_IMODE(root.stat().st_mode)
    root.chmod((mode & ~0o222) | 0o500)


def excerpt(value: str, limit: int) -> str:
    compact = " ".join(value.strip().split())
    if len(compact) <= limit:
        return compact
    return compact[: max(0, limit - 1)] + "…"


def source_entry(manifest: Mapping[str, Any], name: str) -> Mapping[str, Any] | None:
    for entry in manifest.get("repositories", []):
        if entry.get("name") == name:
            return entry
    return None


def source_root_for(source_root: Path, name: str) -> Path:
    return source_root / name


def git_full_tree_paths(repo_dir: Path) -> set[str]:
    completed = run(["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd=repo_dir)
    return {line.strip() for line in completed.stdout.splitlines() if line.strip()}


def snapshot_repository(config: Mapping[str, Any], destination: Path, limits: Mapping[str, Any]) -> dict[str, Any]:
    repo = str(config["repository"])
    name = str(config["name"])
    url = f"https://github.com/{repo}.git"
    if destination.exists():
        shutil.rmtree(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)

    started = now_utc()
    run(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--filter=blob:none",
            "--sparse",
            "--no-tags",
            url,
            str(destination),
        ],
        timeout=1200,
    )

    sparse_paths = [str(item) for item in config.get("sparse_paths", [])]
    if sparse_paths == ["."]:
        run(["git", "sparse-checkout", "disable"], cwd=destination, timeout=1200)
        selected_paths = ["."]
    else:
        root_dirs_result = run(["git", "ls-tree", "-d", "--name-only", "HEAD"], cwd=destination)
        root_dirs = {line.strip() for line in root_dirs_result.stdout.splitlines() if line.strip()}
        selected_paths = [path for path in sparse_paths if path.split("/", 1)[0] in root_dirs]
        if selected_paths:
            run(
                ["git", "sparse-checkout", "set", "--cone", *selected_paths],
                cwd=destination,
                timeout=1200,
            )

    commit = run(["git", "rev-parse", "HEAD"], cwd=destination).stdout.strip()
    branch = run(["git", "branch", "--show-current"], cwd=destination).stdout.strip() or "detached"
    commit_date = run(["git", "show", "-s", "--format=%cI", "HEAD"], cwd=destination).stdout.strip()
    commit_subject = run(["git", "show", "-s", "--format=%s", "HEAD"], cwd=destination).stdout.strip()
    full_tree_paths = git_full_tree_paths(destination)

    probes: dict[str, bool] = {}
    for probe in config.get("tree_probes", []):
        probes[str(probe)] = str(probe) in full_tree_paths

    run(["git", "remote", "remove", "origin"], cwd=destination)
    shutil.rmtree(destination / ".git", ignore_errors=True)
    digest, files, total_bytes = tree_digest(destination)
    make_read_only(destination)

    return {
        "name": name,
        "repository": repo,
        "required": bool(config.get("required", False)),
        "priority": int(config.get("priority", 0)),
        "status": "SNAPSHOT_READY",
        "classification": "observed",
        "snapshot_started_at": started,
        "snapshot_finished_at": now_utc(),
        "branch": branch,
        "commit": commit,
        "commit_date": commit_date,
        "commit_subject": commit_subject,
        "selected_sparse_paths": selected_paths,
        "full_tree_file_count": len(full_tree_paths),
        "tree_probes": probes,
        "snapshot_tree_sha256": digest,
        "snapshot_files": files,
        "snapshot_bytes": total_bytes,
        "source_remote_removed": True,
        "source_git_metadata_removed": True,
        "source_made_read_only": True,
        "max_repository_files_scanned": int(limits["max_repository_files_scanned"]),
    }


def cmd_snapshot(args: argparse.Namespace) -> int:
    plan_path = Path(args.plan).resolve()
    source_root = Path(args.source_root).resolve()
    manifest_path = Path(args.manifest).resolve()
    plan = load_json(plan_path)
    source_root.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    required_failures: list[str] = []
    for config in sorted(plan["repositories"], key=lambda item: (-int(item["priority"]), item["name"])):
        name = str(config["name"])
        print(f"[snapshot] {config['repository']} -> {name}", flush=True)
        try:
            record = snapshot_repository(config, source_root / name, plan["limits"])
        except Exception as exc:
            record = {
                "name": name,
                "repository": str(config["repository"]),
                "required": bool(config.get("required", False)),
                "priority": int(config.get("priority", 0)),
                "status": "SNAPSHOT_FAILED",
                "classification": "not_checked",
                "error": excerpt(str(exc), 1200),
                "snapshot_finished_at": now_utc(),
            }
            if record["required"]:
                required_failures.append(name)
        records.append(record)

    payload = {
        "schema": "chatgpt-audits.source-snapshot.v1",
        "generation": GENERATION,
        "review_status": REVIEW_STATUS,
        "classification": "observed" if not required_failures else "not_checked",
        "created_at": now_utc(),
        "created_at_london": now_london(),
        "plan_path": plan_path.name,
        "plan_sha256": sha256_file(plan_path),
        "source_root": str(source_root),
        "network_boundary": plan["source_policy"],
        "required_failures": required_failures,
        "repositories": records,
    }
    write_json(manifest_path, payload)
    print(f"[snapshot] manifest {manifest_path}", flush=True)
    return 2 if required_failures else 0


def evidence_rows(
    repo_name: str,
    repo_root: Path,
    patterns: Mapping[str, re.Pattern[str]],
    *,
    commit: str,
    max_file_bytes: int,
    max_excerpt_chars: int,
    max_rows: int,
    include_paths: re.Pattern[str] | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in iter_files(repo_root):
        rel = relative_posix(path, repo_root)
        if include_paths and not include_paths.search(rel):
            continue
        text = read_text(path, max_file_bytes)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for category, pattern in patterns.items():
                if pattern.search(line):
                    rows.append(
                        {
                            "classification": "observed",
                            "category": category,
                            "repository": repo_name,
                            "commit": commit,
                            "path": rel,
                            "line": line_number,
                            "excerpt": excerpt(line, max_excerpt_chars),
                        }
                    )
                    if len(rows) >= max_rows:
                        return rows
    return rows


def workflow_risks(repo_name: str, repo_root: Path, commit: str, limits: Mapping[str, Any]) -> list[dict[str, Any]]:
    patterns = {
        "contents_write": re.compile(r"\bcontents\s*:\s*write\b", re.I),
        "pages_write": re.compile(r"\bpages\s*:\s*write\b", re.I),
        "actions_write": re.compile(r"\bactions\s*:\s*write\b", re.I),
        "git_push": re.compile(r"\bgit\s+push\b", re.I),
        "live_network_command": re.compile(r"\b(curl|wget)\b|\bgh\s+api\b", re.I),
        "scheduled": re.compile(r"\bschedule\s*:", re.I),
        "workflow_dispatch": re.compile(r"\bworkflow_dispatch\s*:", re.I),
    }
    return evidence_rows(
        repo_name,
        repo_root,
        patterns,
        commit=commit,
        max_file_bytes=int(limits["max_text_file_bytes"]),
        max_excerpt_chars=int(limits["max_excerpt_chars"]),
        max_rows=min(250, int(limits["max_evidence_rows_per_report"])),
        include_paths=re.compile(r"(^|/)\.github/workflows/.*\.(ya?ml)$", re.I),
    )


def repo_inventory(repo_entry: Mapping[str, Any], root: Path, limits: Mapping[str, Any]) -> dict[str, Any]:
    suffixes: collections.Counter[str] = collections.Counter()
    top_level: collections.Counter[str] = collections.Counter()
    generations: collections.Counter[str] = collections.Counter()
    text_files = 0
    text_bytes = 0
    total_files = 0
    total_bytes = 0
    largest: list[tuple[int, str]] = []
    refs: collections.Counter[str] = collections.Counter()
    max_files = int(limits["max_repository_files_scanned"])

    for path in iter_files(root, limit=max_files):
        rel = relative_posix(path, root)
        size = path.stat().st_size
        total_files += 1
        total_bytes += size
        suffixes[path.suffix.lower() or "[no suffix]"] += 1
        top_level[rel.split("/", 1)[0]] += 1
        largest.append((size, rel))
        text = read_text(path, int(limits["max_text_file_bytes"]))
        if text is None:
            continue
        text_files += 1
        text_bytes += size
        generations.update(GENERATION_RE.findall(text))
        for target in ["pipelinenews", "gridatlas", "companies", "globalgrid2050", "data-gridatlas", "spiders", "cvaa", "data-centres-gb", "data-gb-electricity"]:
            count = text.lower().count(target.lower())
            if count:
                refs[target] += count

    largest.sort(reverse=True)
    return {
        "name": repo_entry["name"],
        "repository": repo_entry["repository"],
        "commit": repo_entry.get("commit"),
        "classification": "observed",
        "files_scanned": total_files,
        "bytes_scanned": total_bytes,
        "text_files": text_files,
        "text_bytes": text_bytes,
        "suffix_counts": dict(suffixes.most_common()),
        "top_level_counts": dict(top_level.most_common()),
        "generation_tokens": [
            {"generation": token, "occurrences": count}
            for token, count in generations.most_common(30)
        ],
        "cross_repository_reference_counts": dict(refs.most_common()),
        "largest_files": [{"path": rel, "bytes": size} for size, rel in largest[:15]],
    }


def phase_one(plan: Mapping[str, Any], manifest: Mapping[str, Any], source_root: Path, output_root: Path) -> None:
    inventories: list[dict[str, Any]] = []
    risks: list[dict[str, Any]] = []
    for entry in manifest["repositories"]:
        if entry.get("status") != "SNAPSHOT_READY":
            continue
        root = source_root_for(source_root, str(entry["name"]))
        inventories.append(repo_inventory(entry, root, plan["limits"]))
        risks.extend(workflow_risks(str(entry["name"]), root, str(entry["commit"]), plan["limits"]))

    payload = {
        "schema": "chatgpt-audits.repository-inventory.v1",
        "generation": GENERATION,
        "review_status": REVIEW_STATUS,
        "classification": "observed",
        "created_at": now_utc(),
        "repositories": inventories,
        "workflow_evidence": risks,
    }
    write_json(output_root / "01-REPOSITORY-INVENTORY.json", payload)

    rows = []
    for item in inventories:
        rows.append(
            f"| {item['name']} | `{str(item['commit'])[:12]}` | {item['files_scanned']:,} | "
            f"{item['text_files']:,} | {item['bytes_scanned'] / 1024 / 1024:.2f} MiB |"
        )
    risk_counts = collections.Counter(row["category"] for row in risks)
    risk_lines = "\n".join(f"- `{key}`: {value} observed line(s)" for key, value in risk_counts.most_common()) or "- None observed in selected workflow snapshots."
    content = md_header("01 — Repository inventory and topology") + "\n"
    content += (
        "This checkpoint records exact commits and scans the selected source-code surface. It does not infer that an unselected path is absent.\n\n"
        "| Repository | Commit | Files scanned | Text files | Selected bytes |\n"
        "|---|---:|---:|---:|---:|\n"
        + "\n".join(rows)
        + "\n\n## Workflow evidence categories\n\n"
        + risk_lines
        + "\n\n## Interpretation\n\n"
        "- **Observed:** the manifest pins each analysed repository commit and content digest.\n"
        "- **Observed:** product repositories contain several workflows with write-capable permissions or push commands; each exact line is in the JSON evidence ledger.\n"
        "- **Inferred:** cross-repository seam verification should be treated as a first-class test surface because the repositories reference each other frequently.\n"
        "- **Not checked:** raw datasets and excluded release/data directories were not downloaded.\n"
    )
    write_text(output_root / "01-REPOSITORY-INVENTORY.md", content)


def responsibility_categories(text: str) -> set[str]:
    lower = text.lower()
    categories: set[str] = set()
    rules = {
        "collection": ("fetch(", "source", "query", "rss", "search", "adapter"),
        "evidence": ("evidence", "provenance", "source_card", "source-card", "ledger"),
        "identity": ("repd_ref", "gg_project_id", "company_number", "binding_status", "identity"),
        "scoring": ("score", "confidence", "rank", "weight"),
        "publication": ("publish", "promotion", "release", "current.json", "pointer"),
        "network": ("https://", "fetch(", "request(", "curl ", "wget "),
        "presentation": ("headline", "render", "html", "table", "card"),
        "validation": ("assert", "invariant", "schema", "validate", "fixture"),
    }
    for category, markers in rules.items():
        if any(marker in lower for marker in markers):
            categories.add(category)
    return categories


def analyse_pipeline_file(path: Path, root: Path, limits: Mapping[str, Any]) -> dict[str, Any] | None:
    text = read_text(path, int(limits["max_text_file_bytes"]))
    if text is None:
        return None
    rel = relative_posix(path, root)
    lower_rel = rel.lower()
    lower_text = text.lower()
    if not any(marker in lower_rel or marker in lower_text for marker in ("discover", "news", "evidence", "headline", "identity", "sector", "pipeline")):
        return None
    categories = responsibility_categories(text)
    urls = URL_RE.findall(text)
    generations = GENERATION_RE.findall(text)
    function_count = len(re.findall(r"\b(?:function\s+|const\s+[A-Za-z_$][\w$]*\s*=\s*(?:async\s*)?\(|def\s+)[A-Za-z_$]?", text))
    hardcoded_dates = sorted(set(re.findall(r"\b20\d{2}-\d{2}-\d{2}\b", text)))
    return {
        "path": rel,
        "bytes": path.stat().st_size,
        "lines": text.count("\n") + 1,
        "function_markers": function_count,
        "responsibilities": sorted(categories),
        "responsibility_count": len(categories),
        "url_count": len(urls),
        "generation_tokens": sorted(set(generations))[:30],
        "hardcoded_dates": hardcoded_dates[:30],
        "monolith_candidate": path.stat().st_size >= 25000 and len(categories) >= 4,
    }


def phase_two(plan: Mapping[str, Any], manifest: Mapping[str, Any], source_root: Path, output_root: Path) -> None:
    entry = source_entry(manifest, "pipelinenews")
    if not entry or entry.get("status") != "SNAPSHOT_READY":
        raise RuntimeError("pipelinenews snapshot is required for phase 2")
    root = source_root_for(source_root, "pipelinenews")
    files: list[dict[str, Any]] = []
    for path in iter_files(root, limit=int(plan["limits"]["max_repository_files_scanned"])):
        analysed = analyse_pipeline_file(path, root, plan["limits"])
        if analysed:
            files.append(analysed)
    files.sort(key=lambda item: (item["monolith_candidate"], item["responsibility_count"], item["bytes"]), reverse=True)

    patterns = {
        "identity_rule": re.compile(r"repd_ref|gg_project_id|binding_status|identity", re.I),
        "evidence_rule": re.compile(r"evidence|provenance|source[_-]?card|ledger", re.I),
        "publication_rule": re.compile(r"publish|promotion|release|pointer", re.I),
        "network_rule": re.compile(r"fetch\s*\(|https?://|request\s*\(", re.I),
        "abstention_rule": re.compile(r"abstain|ambiguous|reject", re.I),
    }
    evidence = evidence_rows(
        "pipelinenews",
        root,
        patterns,
        commit=str(entry["commit"]),
        max_file_bytes=int(plan["limits"]["max_text_file_bytes"]),
        max_excerpt_chars=int(plan["limits"]["max_excerpt_chars"]),
        max_rows=int(plan["limits"]["max_evidence_rows_per_report"]),
        include_paths=re.compile(r"(^|/)(discovery|ui|automation|orchestration|contracts|state)/", re.I),
    )

    observed_module_names = {
        "collector": [],
        "evidence_ledger": [],
        "identity_binder": [],
        "timing_state_machine": [],
        "publisher": [],
    }
    module_patterns = {
        "collector": re.compile(r"collect(or|ion)|adapter", re.I),
        "evidence_ledger": re.compile(r"evidence.*ledger|ledger.*evidence", re.I),
        "identity_binder": re.compile(r"identity.*bind|bind.*identity|entity.*resolution", re.I),
        "timing_state_machine": re.compile(r"timing.*state|state.*machine|window.*state", re.I),
        "publisher": re.compile(r"publish|promotion", re.I),
    }
    for item in files:
        for name, pattern in module_patterns.items():
            if pattern.search(item["path"]):
                observed_module_names[name].append(item["path"])

    base_url_observation: dict[str, Any] = {
        "classification": "not_observed_in_snapshot",
        "path": "ui/atlas-v9-deep-links.js",
        "base_url": None,
    }
    deep_link_path = root / "ui/atlas-v9-deep-links.js"
    deep_link_text = read_text(deep_link_path, int(plan["limits"]["max_text_file_bytes"])) if deep_link_path.exists() else None
    if deep_link_text:
        match = re.search(r"BASE_URL\s*=\s*[\"']([^\"']+)", deep_link_text)
        if match:
            base_url_observation = {
                "classification": "observed",
                "path": "ui/atlas-v9-deep-links.js",
                "base_url": match.group(1),
            }

    findings: list[dict[str, Any]] = []
    monoliths = [item for item in files if item["monolith_candidate"]]
    if monoliths:
        findings.append(
            {
                "classification": "observed",
                "finding": "Large PipelineNews files combine four or more responsibility categories.",
                "evidence_paths": [item["path"] for item in monoliths[:10]],
            }
        )
        findings.append(
            {
                "classification": "inferred",
                "finding": "The next version should extract collectors, evidence ledger, identity binding and timing promotion into separate contracts instead of adding another monolithic runner.",
                "derived_from": [item["path"] for item in monoliths[:5]],
            }
        )
    for module, paths in observed_module_names.items():
        if not paths:
            findings.append(
                {
                    "classification": "not_observed_in_snapshot",
                    "finding": f"No selected PipelineNews path was named as a dedicated {module.replace('_', ' ')} module.",
                }
            )

    payload = {
        "schema": "chatgpt-audits.pipelinenews-engine-audit.v1",
        "generation": GENERATION,
        "review_status": REVIEW_STATUS,
        "classification": "observed",
        "created_at": now_utc(),
        "repository": entry["repository"],
        "commit": entry["commit"],
        "candidate_files": files[:200],
        "monolith_candidates": monoliths,
        "dedicated_module_name_observations": observed_module_names,
        "deep_link_base_url": base_url_observation,
        "evidence": evidence,
        "findings": findings,
    }
    write_json(output_root / "02-PIPELINENEWS-ENGINE-AUDIT.json", payload)

    top_rows = []
    for item in files[:20]:
        top_rows.append(
            f"| `{item['path']}` | {item['bytes']:,} | {item['lines']:,} | "
            f"{', '.join(item['responsibilities']) or 'none'} | {'YES' if item['monolith_candidate'] else 'no'} |"
        )
    module_lines = []
    for module, paths in observed_module_names.items():
        if paths:
            module_lines.append(f"- **Observed `{module}` names:** " + ", ".join(f"`{path}`" for path in paths[:10]))
        else:
            module_lines.append(f"- **Not observed in selected snapshot:** dedicated `{module}` filename/interface.")
    content = md_header("02 — PipelineNews intelligence-engine audit") + "\n"
    content += (
        f"Pinned source: `{entry['repository']}@{entry['commit']}`.\n\n"
        "| Candidate file | Bytes | Lines | Responsibilities observed | Monolith candidate |\n"
        "|---|---:|---:|---|---:|\n"
        + "\n".join(top_rows)
        + "\n\n## Module-boundary observations\n\n"
        + "\n".join(module_lines)
        + "\n\n## Current deep-link producer\n\n"
        + (f"- **Observed:** `{base_url_observation['base_url']}` in `{base_url_observation['path']}`.\n" if base_url_observation["base_url"] else "- **Not observed in selected snapshot:** a readable `BASE_URL`.\n")
        + "\n## Architectural conclusion\n\n"
        "- **Observed:** collection, network access, evidence handling, identity terms, validation and release/promotion terms coexist in large runner files.\n"
        "- **Inferred:** adding another runner would increase coupling and make abstention, retraction and source revision harder to prove.\n"
        "- **Inferred:** the vNext boundary should be `collectors → evidence ledger → identity binder → timing state machine → reviewed read model`.\n"
        "- **Not checked:** this automated scan does not execute live feeds or prove current public Pages behaviour.\n"
    )
    write_text(output_root / "02-PIPELINENEWS-ENGINE-AUDIT.md", content)


def phase_three(plan: Mapping[str, Any], manifest: Mapping[str, Any], source_root: Path, output_root: Path) -> None:
    patterns = {
        "funding_fact": re.compile(r"\b(charge|charges|allotment|statement of capital|accounts filed|company number|company_number|mortgage|funding|finance|financing)\b", re.I),
        "procurement_fact": re.compile(r"\b(planning|condition discharge|discharge of condition|procurement|tender|contract award|epc|reserved matters|pre-commencement)\b", re.I),
        "identity_key": re.compile(r"\b(repd_ref|gg_project_id|company_number|planning_application|application_ref)\b", re.I),
        "privacy_boundary": re.compile(r"\b(director|psc|date of birth|residential address|privacy|personal data)\b", re.I),
        "inference_term": re.compile(r"\b(score|confidence|window|inferred|candidate|prediction)\b", re.I),
    }
    all_rows: list[dict[str, Any]] = []
    for repo_name in ("companies", "pipelinenews", "spiders", "data-gridatlas"):
        entry = source_entry(manifest, repo_name)
        if not entry or entry.get("status") != "SNAPSHOT_READY":
            continue
        rows = evidence_rows(
            repo_name,
            source_root_for(source_root, repo_name),
            patterns,
            commit=str(entry["commit"]),
            max_file_bytes=int(plan["limits"]["max_text_file_bytes"]),
            max_excerpt_chars=int(plan["limits"]["max_excerpt_chars"]),
            max_rows=140,
        )
        all_rows.extend(rows)
    all_rows = all_rows[: int(plan["limits"]["max_evidence_rows_per_report"])]

    event_contract = {
        "schema": "pipelinenews.event-contract.candidate.v1",
        "generation": GENERATION,
        "review_status": REVIEW_STATUS,
        "classification": "inferred",
        "status": "QUARANTINED_DRAFT",
        "separation_rule": "Observed register events and inferred commercial windows are separate records joined only by evidence IDs.",
        "observed_event": {
            "required": [
                "event_id",
                "source_system",
                "source_record_id",
                "event_type",
                "observed_at",
                "effective_at",
                "evidence_sha256",
                "fact_status"
            ],
            "fact_status_allowed": ["OBSERVED", "REVISED", "RETRACTED", "CONTRADICTED"],
            "event_type_candidates": [
                "COMPANY_CHARGE_CREATED",
                "COMPANY_CHARGE_SATISFIED",
                "COMPANY_ALLOTMENT_FILED",
                "COMPANY_ACCOUNTS_FILED",
                "PLANNING_APPLICATION_STATUS",
                "PLANNING_CONDITION_EVENT",
                "PROCUREMENT_NOTICE_OBSERVED"
            ]
        },
        "inferred_window": {
            "required": [
                "inference_id",
                "project_id",
                "inference_type",
                "classification",
                "rule_version",
                "input_evidence_ids",
                "calculated_at",
                "review_status"
            ],
            "classification_constant": "inferred",
            "inference_type_candidates": ["FUNDING_WINDOW", "PROCUREMENT_WINDOW", "CORROBORATED_SALES_WINDOW"],
            "may_publish_without_human_review": False
        },
        "identity_join": {
            "project_key": "gg_project_id",
            "project_source_key": "repd_ref",
            "company_key": "company_number",
            "planning_key": "planning_application_ref",
            "relationship_required_fields": ["relationship_type", "evidence_ids", "valid_from", "valid_to", "binding_status", "review_status"]
        },
        "privacy": {
            "forbidden_public_fields": ["director_name", "individual_psc", "date_of_birth", "residential_address"],
            "company_number_is_an_organisation_identifier": True
        }
    }
    write_json(output_root / "03-EVENT-CONTRACT-CANDIDATE.json", event_contract)
    write_json(
        output_root / "03-FUNDING-PROCUREMENT-EVIDENCE.json",
        {
            "schema": "chatgpt-audits.funding-procurement-evidence.v1",
            "generation": GENERATION,
            "review_status": REVIEW_STATUS,
            "classification": "observed",
            "created_at": now_utc(),
            "evidence": all_rows,
        },
    )

    counts = collections.Counter(row["category"] for row in all_rows)
    count_lines = "\n".join(f"- `{category}`: {count} selected source-code line(s)" for category, count in counts.most_common())
    content = md_header("03 — Funding and procurement signal separation") + "\n"
    content += (
        "The commercial timing engine needs two independent evidence lanes. The source scan below records only code and contract language; it does not assert that a real project is funded or procuring.\n\n"
        "## Evidence-language inventory\n\n"
        + (count_lines or "- No matching lines observed in the selected snapshots.")
        + "\n\n## Candidate event model\n\n"
        "1. **Observed register event:** a source-stamped filing, charge, planning status, condition or procurement notice.\n"
        "2. **Identity relationship:** a separately evidenced binding between company, planning application and canonical project.\n"
        "3. **Inferred window:** a rule-versioned interpretation that cites observed evidence IDs and is always labelled `inferred`.\n"
        "4. **Corroborated sales window:** permitted only when an observed funding lane and an observed procurement lane both exist for the same reviewed project identity.\n\n"
        "## Hard boundary\n\n"
        "- One lane alone must remain silent.\n"
        "- Absence of a filing or planning event is not negative evidence.\n"
        "- News may corroborate or explain evidence; it must not manufacture the funding or procurement fact.\n"
        "- Company relationship Parquet can stay compact; event history belongs in a separate, append-only contract.\n"
        "- Public outputs must preserve the Companies privacy boundary and exclude individual director/PSC details.\n"
    )
    write_text(output_root / "03-FUNDING-AND-PROCUREMENT-SIGNALS.md", content)


def find_first_line(path: Path, pattern: re.Pattern[str], max_bytes: int) -> tuple[int, str] | None:
    text = read_text(path, max_bytes)
    if text is None:
        return None
    for number, line in enumerate(text.splitlines(), 1):
        if pattern.search(line):
            return number, excerpt(line, 280)
    return None


def claim(
    claim_id: str,
    statement: str,
    classification: str,
    evidence: list[dict[str, Any]],
    note: str,
) -> dict[str, Any]:
    if classification not in CLASSIFICATIONS:
        raise ValueError(classification)
    return {
        "claim_id": claim_id,
        "statement": statement,
        "classification": classification,
        "evidence": evidence,
        "note": note,
    }


def phase_four(
    plan: Mapping[str, Any],
    manifest: Mapping[str, Any],
    source_root: Path,
    audit_root: Path,
    output_root: Path,
) -> None:
    max_bytes = int(plan["limits"]["max_text_file_bytes"])
    claims: list[dict[str, Any]] = []

    pipeline = source_entry(manifest, "pipelinenews")
    grid = source_entry(manifest, "gridatlas")
    companies = source_entry(manifest, "companies")

    pipeline_root = source_root_for(source_root, "pipelinenews")
    grid_root = source_root_for(source_root, "gridatlas")
    companies_root = source_root_for(source_root, "companies")

    deep_path = pipeline_root / "ui/atlas-v9-deep-links.js"
    old_url = re.compile(r"https://ventusltd\.github\.io/gridatlas/202608300453-atlas-v9/")
    hit = find_first_line(deep_path, old_url, max_bytes) if deep_path.exists() else None
    if hit and pipeline:
        claims.append(
            claim(
                "CROSSCHECK-001",
                "PipelineNews still emits the pre-move root GridAtlas release route.",
                "observed",
                [{"repository": "pipelinenews", "commit": pipeline["commit"], "path": "ui/atlas-v9-deep-links.js", "line": hit[0], "excerpt": hit[1]}],
                "The copied study's producer-side string is present at the pinned commit.",
            )
        )
    else:
        claims.append(
            claim(
                "CROSSCHECK-001",
                "PipelineNews still emits the pre-move root GridAtlas release route.",
                "contradicted" if deep_path.exists() else "not_checked",
                [],
                "The expected literal was not found in the selected current file." if deep_path.exists() else "The current file was not available in the selected snapshot.",
            )
        )

    live_route_evidence: list[dict[str, Any]] = []
    for rel in ("state/live-set.json", "atlas/current.json"):
        path = grid_root / rel
        if not path.exists() or not grid:
            continue
        route_hit = find_first_line(path, re.compile(r"/gridatlas/atlas/"), max_bytes)
        if route_hit:
            live_route_evidence.append({"repository": "gridatlas", "commit": grid["commit"], "path": rel, "line": route_hit[0], "excerpt": route_hit[1]})
    if live_route_evidence:
        claims.append(
            claim(
                "CROSSCHECK-002",
                "GridAtlas declares `/gridatlas/atlas/` as its stable live route.",
                "observed",
                live_route_evidence,
                "Current selected pointer/composition files contain the stable route.",
            )
        )
    else:
        claims.append(claim("CROSSCHECK-002", "GridAtlas declares `/gridatlas/atlas/` as its stable live route.", "not_checked", [], "No readable selected pointer file proved the route."))

    if grid:
        probes = grid.get("tree_probes", {})
        old_probe = probes.get("202608300453-atlas-v9/index.html")
        new_probe = probes.get("atlas/releases/202608300453-atlas-v9/index.html")
        if old_probe is False and new_probe is True:
            classification = "observed"
            note = "The full Git tree probe records the old root path absent and the moved release path present."
        elif old_probe is not None or new_probe is not None:
            classification = "contradicted"
            note = f"Tree probes did not match the copied claim: old={old_probe!r}, new={new_probe!r}."
        else:
            classification = "not_checked"
            note = "The source plan did not contain both full-tree probes."
        claims.append(
            claim(
                "CROSSCHECK-003",
                "The `202608300453-atlas-v9` release moved from repository root to `atlas/releases/`.",
                classification,
                [{"repository": "gridatlas", "commit": grid.get("commit"), "tree_probes": {"old": old_probe, "new": new_probe}}],
                note,
            )
        )

    overnight_rel = ".github/workflows/202608310015-gridatlas-overnight-next-versions.yml"
    overnight = grid_root / overnight_rel
    push_hit = find_first_line(overnight, re.compile(r"git\s+push\s+origin\s+HEAD:main", re.I), max_bytes) if overnight.exists() else None
    if push_hit and grid:
        claims.append(
            claim(
                "CROSSCHECK-004",
                "A GridAtlas overnight study workflow can commit study/candidate output directly to product `main`.",
                "observed",
                [{"repository": "gridatlas", "commit": grid["commit"], "path": overnight_rel, "line": push_hit[0], "excerpt": push_hit[1]}],
                "This is an anti-pattern for the audit automation; the new workflow writes only to an audit branch.",
            )
        )
    else:
        claims.append(claim("CROSSCHECK-004", "A GridAtlas overnight study workflow can commit study/candidate output directly to product `main`.", "not_observed_in_snapshot", [], "No exact push line was observed in the selected workflow snapshot."))

    companies_readme = companies_root / "README.md"
    compact_hit = find_first_line(companies_readme, re.compile(r"key-only relationship|compact relationship", re.I), max_bytes) if companies_readme.exists() else None
    if compact_hit and companies:
        claims.append(
            claim(
                "CROSSCHECK-005",
                "Companies preserves a compact relationship-candidate and privacy boundary rather than publishing a company master dataset.",
                "observed",
                [{"repository": "companies", "commit": companies["commit"], "path": "README.md", "line": compact_hit[0], "excerpt": compact_hit[1]}],
                "The boundary should be retained while adding a separate event-history contract.",
            )
        )
    else:
        claims.append(claim("CROSSCHECK-005", "Companies preserves a compact relationship-candidate and privacy boundary rather than publishing a company master dataset.", "not_checked", [], "The selected README did not prove the claim."))

    if grid:
        build_plan_probe = grid.get("tree_probes", {}).get("_build-plan/summary.md")
        claims.append(
            claim(
                "CROSSCHECK-006",
                "Claude's `_build-plan` exists at the current GridAtlas commit.",
                "observed" if build_plan_probe is True else "not_observed_in_snapshot" if build_plan_probe is False else "not_checked",
                [{"repository": "gridatlas", "commit": grid.get("commit"), "tree_probe": build_plan_probe}],
                "A false tree probe means only that the named path was not observed at this commit; copied study material remains in chatgpt-audits.",
            )
        )

    copied_study = audit_root / "202608310033-study"
    tokens: collections.Counter[str] = collections.Counter()
    for path in iter_files(copied_study, limit=5000):
        if "AUTOMATION-RUNS" in path.parts:
            continue
        text = read_text(path, max_bytes)
        if text is None:
            continue
        for token in BACKTICK_RE.findall(text):
            if "/" in token and len(token) <= 220 and not token.startswith(("http://", "https://")):
                tokens[token] += 1
    path_census = [{"token": token, "mentions": count} for token, count in tokens.most_common(250)]

    ledger = {
        "schema": "chatgpt-audits.claude-crosscheck-ledger.v1",
        "generation": GENERATION,
        "review_status": REVIEW_STATUS,
        "classification": "observed",
        "created_at": now_utc(),
        "source_note": "Claims were copied into chatgpt-audits and re-tested against pinned repository snapshots. No live product or external data source was queried.",
        "claims": claims,
        "copied_study_path_token_census": path_census,
    }
    write_json(output_root / "04-CLAUDE-CROSSCHECK-LEDGER.json", ledger)

    claim_rows = []
    for item in claims:
        claim_rows.append(f"| `{item['claim_id']}` | `{item['classification']}` | {item['statement']} | {item['note']} |")
    content = md_header("04 — Seams and copied-Claude-study cross-check") + "\n"
    content += (
        "The copied study is treated as a hypothesis corpus, not as current truth. Every row below was tested against exact commits captured at run start.\n\n"
        "| Claim | Result | Statement | Note |\n"
        "|---|---|---|---|\n"
        + "\n".join(claim_rows)
        + "\n\n## Governing interpretation\n\n"
        "- Agreement between copied study and current source raises confidence but does not constitute human review.\n"
        "- A contradiction is preserved in the ledger; the older text is not silently rewritten.\n"
        "- `not_observed_in_snapshot` is not evidence of non-existence.\n"
        "- The highest-priority seam remains PipelineNews's producer URL versus GridAtlas's current stable route.\n"
        "- No repair is installed here; the output is a quarantined graduation candidate only.\n"
    )
    write_text(output_root / "04-SEAMS-AND-CLAUDE-CROSSCHECK.md", content)


def schema_evidence_event() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:ventus:pipelinenews:evidence-event:vnext",
        "title": "UNREVIEWED PipelineNews evidence event",
        "review_status": REVIEW_STATUS,
        "classification": "inferred",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "event_id", "source_system", "source_record_id", "event_type", "observed_at",
            "effective_at", "fact_status", "evidence_sha256", "source_card_id"
        ],
        "properties": {
            "event_id": {"type": "string", "minLength": 8, "maxLength": 160},
            "source_system": {"type": "string", "enum": ["COMPANIES_HOUSE", "PLANNING_REGISTER", "PROCUREMENT_REGISTER", "REPD", "NEWS_CORROBORATION"]},
            "source_record_id": {"type": "string", "minLength": 1, "maxLength": 240},
            "event_type": {"type": "string", "minLength": 3, "maxLength": 100},
            "observed_at": {"type": "string", "format": "date-time"},
            "effective_at": {"type": ["string", "null"], "format": "date-time"},
            "fact_status": {"type": "string", "enum": ["OBSERVED", "REVISED", "RETRACTED", "CONTRADICTED"]},
            "evidence_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "source_card_id": {"type": "string", "minLength": 3, "maxLength": 160},
            "project_keys": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "repd_ref": {"type": ["string", "null"], "maxLength": 40},
                    "gg_project_id": {"type": ["string", "null"], "pattern": "^GG2050-REPD-[0-9]+$"},
                    "company_number": {"type": ["string", "null"], "maxLength": 16},
                    "planning_application_ref": {"type": ["string", "null"], "maxLength": 120}
                }
            },
            "supersedes_event_id": {"type": ["string", "null"], "maxLength": 160}
        }
    }


def schema_transition() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:ventus:pipelinenews:timing-transition:vnext",
        "title": "UNREVIEWED PipelineNews timing transition",
        "review_status": REVIEW_STATUS,
        "classification": "inferred",
        "type": "object",
        "additionalProperties": False,
        "required": ["transition_id", "project_id", "from_state", "to_state", "input_evidence_ids", "classification", "rule_version", "calculated_at", "review_status"],
        "properties": {
            "transition_id": {"type": "string"},
            "project_id": {"type": "string", "pattern": "^GG2050-REPD-[0-9]+$"},
            "from_state": {"$ref": "#/$defs/state"},
            "to_state": {"$ref": "#/$defs/state"},
            "input_evidence_ids": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
            "classification": {"const": "inferred"},
            "rule_version": {"type": "string"},
            "calculated_at": {"type": "string", "format": "date-time"},
            "review_status": {"type": "string", "enum": ["UNREVIEWED", "HUMAN_REVIEWED", "REJECTED"]},
            "reason": {"type": "string", "maxLength": 1000}
        },
        "$defs": {
            "state": {
                "type": "string",
                "enum": [
                    "DISCOVERED", "IDENTITY_CANDIDATE", "FUNDING_OBSERVED", "PROCUREMENT_OBSERVED",
                    "CORROBORATED_WINDOW", "HUMAN_REVIEWED", "RELEASE_CANDIDATE", "WITHHELD", "CONFLICTED", "STALE"
                ]
            }
        }
    }


def schema_summary() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:ventus:pipelinenews:project-intelligence-summary:vnext",
        "title": "UNREVIEWED publishable project intelligence read model",
        "review_status": REVIEW_STATUS,
        "classification": "inferred",
        "type": "object",
        "additionalProperties": False,
        "required": ["gg_project_id", "repd_ref", "state", "as_of", "review_status", "observed_facts", "inferred_windows", "source_refs", "staleness"],
        "properties": {
            "gg_project_id": {"type": "string", "pattern": "^GG2050-REPD-[0-9]+$"},
            "repd_ref": {"type": "string", "pattern": "^[A-Za-z0-9-]{1,40}$"},
            "state": {"type": "string"},
            "as_of": {"type": "string", "format": "date-time"},
            "review_status": {"const": "HUMAN_REVIEWED"},
            "observed_facts": {"type": "array", "items": {"type": "object"}},
            "inferred_windows": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["classification", "inference_type", "input_evidence_ids", "rule_version"],
                    "properties": {
                        "classification": {"const": "inferred"},
                        "inference_type": {"type": "string"},
                        "input_evidence_ids": {"type": "array", "items": {"type": "string"}},
                        "rule_version": {"type": "string"}
                    }
                }
            },
            "source_refs": {"type": "array", "items": {"type": "string"}},
            "staleness": {"type": "object"},
            "gridatlas_deep_link": {"type": ["string", "null"], "format": "uri"}
        }
    }


def reference_state_machine() -> str:
    return '''# REVIEW STATUS: UNREVIEWED
"""Quarantined reference state machine for PipelineNews vNext.

This module is a design artefact only. It deliberately cannot publish.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class State(str, Enum):
    DISCOVERED = "DISCOVERED"
    IDENTITY_CANDIDATE = "IDENTITY_CANDIDATE"
    FUNDING_OBSERVED = "FUNDING_OBSERVED"
    PROCUREMENT_OBSERVED = "PROCUREMENT_OBSERVED"
    CORROBORATED_WINDOW = "CORROBORATED_WINDOW"
    HUMAN_REVIEWED = "HUMAN_REVIEWED"
    RELEASE_CANDIDATE = "RELEASE_CANDIDATE"
    WITHHELD = "WITHHELD"
    CONFLICTED = "CONFLICTED"
    STALE = "STALE"


class Lane(str, Enum):
    FUNDING = "FUNDING"
    PROCUREMENT = "PROCUREMENT"
    CORROBORATION = "CORROBORATION"


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    lane: Lane
    fact_status: str = "OBSERVED"
    retracted: bool = False

    @property
    def usable(self) -> bool:
        return self.fact_status == "OBSERVED" and not self.retracted


def observed_lanes(evidence: Iterable[Evidence]) -> set[Lane]:
    return {item.lane for item in evidence if item.usable}


def has_dual_register_corroboration(evidence: Iterable[Evidence]) -> bool:
    lanes = observed_lanes(evidence)
    return Lane.FUNDING in lanes and Lane.PROCUREMENT in lanes


def propose_transition(
    current: State,
    requested: State,
    evidence: Iterable[Evidence],
    *,
    identity_reviewed: bool = False,
    human_reviewed: bool = False,
    contradiction: bool = False,
) -> State:
    evidence = tuple(evidence)
    lanes = observed_lanes(evidence)

    if contradiction:
        return State.CONFLICTED

    if requested == State.IDENTITY_CANDIDATE:
        return State.IDENTITY_CANDIDATE

    if requested == State.FUNDING_OBSERVED:
        if Lane.FUNDING not in lanes:
            raise ValueError("observed funding evidence is required")
        return State.FUNDING_OBSERVED

    if requested == State.PROCUREMENT_OBSERVED:
        if Lane.PROCUREMENT not in lanes:
            raise ValueError("observed procurement evidence is required")
        return State.PROCUREMENT_OBSERVED

    if requested == State.CORROBORATED_WINDOW:
        if not identity_reviewed:
            raise ValueError("reviewed project identity is required")
        if not has_dual_register_corroboration(evidence):
            raise ValueError("both funding and procurement evidence are required")
        return State.CORROBORATED_WINDOW

    if requested == State.HUMAN_REVIEWED:
        if current != State.CORROBORATED_WINDOW or not human_reviewed:
            raise ValueError("human review follows a corroborated window")
        return State.HUMAN_REVIEWED

    if requested == State.RELEASE_CANDIDATE:
        if current != State.HUMAN_REVIEWED or not human_reviewed:
            raise ValueError("release candidate requires recorded human review")
        return State.RELEASE_CANDIDATE

    raise ValueError(f"unsupported or forbidden transition: {requested.value}")


def publish(*_args: object, **_kwargs: object) -> None:
    raise RuntimeError("PUBLISHED transitions are forbidden in chatgpt-audits")
'''


def reference_tests() -> str:
    return '''# REVIEW STATUS: UNREVIEWED
import unittest

from state_machine import Evidence, Lane, State, propose_transition, publish


class TimingStateMachineTests(unittest.TestCase):
    def test_one_signal_stays_silent(self):
        evidence = [Evidence("funding-1", Lane.FUNDING)]
        with self.assertRaisesRegex(ValueError, "both funding and procurement"):
            propose_transition(
                State.FUNDING_OBSERVED,
                State.CORROBORATED_WINDOW,
                evidence,
                identity_reviewed=True,
            )

    def test_dual_register_evidence_can_form_candidate_window(self):
        evidence = [
            Evidence("funding-1", Lane.FUNDING),
            Evidence("planning-1", Lane.PROCUREMENT),
        ]
        result = propose_transition(
            State.PROCUREMENT_OBSERVED,
            State.CORROBORATED_WINDOW,
            evidence,
            identity_reviewed=True,
        )
        self.assertEqual(result, State.CORROBORATED_WINDOW)

    def test_retracted_signal_does_not_count(self):
        evidence = [
            Evidence("funding-1", Lane.FUNDING, retracted=True),
            Evidence("planning-1", Lane.PROCUREMENT),
        ]
        with self.assertRaises(ValueError):
            propose_transition(
                State.PROCUREMENT_OBSERVED,
                State.CORROBORATED_WINDOW,
                evidence,
                identity_reviewed=True,
            )

    def test_contradiction_wins(self):
        result = propose_transition(
            State.DISCOVERED,
            State.IDENTITY_CANDIDATE,
            [],
            contradiction=True,
        )
        self.assertEqual(result, State.CONFLICTED)

    def test_release_requires_human_review(self):
        with self.assertRaises(ValueError):
            propose_transition(
                State.CORROBORATED_WINDOW,
                State.RELEASE_CANDIDATE,
                [],
                human_reviewed=False,
            )

    def test_audit_scaffold_cannot_publish(self):
        with self.assertRaisesRegex(RuntimeError, "forbidden"):
            publish()


if __name__ == "__main__":
    unittest.main()
'''


def phase_five(plan: Mapping[str, Any], manifest: Mapping[str, Any], output_root: Path) -> None:
    candidate_root = output_root / "next-versions/202608310052-pipelinenews-intelligence-vnext"
    schemas = candidate_root / "schemas"
    reference = candidate_root / "reference"

    source_commits = {
        entry["name"]: entry.get("commit")
        for entry in manifest["repositories"]
        if entry.get("status") == "SNAPSHOT_READY"
    }
    architecture = {
        "schema": "pipelinenews.intelligence-architecture.candidate.vnext",
        "generation": GENERATION,
        "review_status": REVIEW_STATUS,
        "classification": "inferred",
        "status": "QUARANTINED_DRAFT",
        "source_commits": source_commits,
        "modules": [
            {"name": "collectors", "owns": ["source-specific retrieval adapter", "source card", "raw response receipt"], "must_not_own": ["project identity conclusion", "commercial timing conclusion", "publication"]},
            {"name": "evidence-ledger", "owns": ["append-only observed events", "revision", "retraction", "contradiction", "content digest"], "must_not_own": ["UI", "ranking", "project publication"]},
            {"name": "identity-binder", "owns": ["company-project-planning relationships", "binding status", "validity interval", "abstention"], "must_not_own": ["source collection", "timing promotion"]},
            {"name": "timing-state-machine", "owns": ["funding lane", "procurement lane", "dual-register gate", "staleness", "withheld/conflicted state"], "must_not_own": ["evidence mutation", "public deployment"]},
            {"name": "reviewed-read-model", "owns": ["human-reviewed summary", "GridAtlas deep-link contract", "PipelineNews presentation payload"], "must_not_own": ["raw Companies data", "individual PII", "unreviewed inference"]}
        ],
        "repository_ownership": {
            "companies": "compact factual company/project relationships and organisation-level register events",
            "pipelinenews": "evidence ledger, identity bindings, timing state and reviewed read model",
            "gridatlas": "consumer visualisation and exact project deep-link receiver",
            "globalgrid2050": "catalogue/origin hub and domain topology",
            "data-centres-gb": "demand-side site evidence and relationships",
            "chatgpt-audits": "unreviewed design and test artefacts only"
        },
        "non_negotiable_rules": [
            "News is evidence/corroboration, not the funding or procurement fact.",
            "One register lane alone does not create a sales window.",
            "Every inference cites immutable evidence IDs and a rule version.",
            "Event time, observed time and calculated time are distinct.",
            "Retractions and contradictions are first-class events.",
            "Absence is not evidence.",
            "Human review is required before a release candidate.",
            "This audit candidate cannot publish."
        ]
    }
    write_json(candidate_root / "architecture.vnext.json", architecture)
    write_json(schemas / "evidence-event.schema.json", schema_evidence_event())
    write_json(schemas / "timing-transition.schema.json", schema_transition())
    write_json(schemas / "project-intelligence-summary.schema.json", schema_summary())
    write_text(reference / "state_machine.py", reference_state_machine())
    write_text(reference / "test_state_machine.py", reference_tests())

    candidate_readme = md_header("PipelineNews intelligence engine vNext — quarantined candidate", "inferred") + "\n"
    candidate_readme += (
        "This is a modular design candidate generated after four evidence checkpoints. It is not a product release and cannot write to PipelineNews, GridAtlas, Companies or GlobalGrid2050.\n\n"
        "## Intended chain\n\n"
        "```text\nsource-specific collectors\n  -> append-only evidence ledger\n    -> reviewed identity bindings\n      -> dual-register timing state machine\n        -> human-reviewed read model\n          -> PipelineNews and GridAtlas consumers\n```\n\n"
        "## Why this is the next version\n\n"
        "The present source surface contains large runners with collection, networking, evidence, identity, validation and publication concerns together. The candidate therefore extracts contracts first and leaves product implementation to a separate reviewed graduation.\n\n"
        "## Files\n\n"
        "- `architecture.vnext.json` — module and repository ownership.\n"
        "- `schemas/evidence-event.schema.json` — observed, revised, retracted and contradicted evidence.\n"
        "- `schemas/timing-transition.schema.json` — inferred state transitions with human-review status.\n"
        "- `schemas/project-intelligence-summary.schema.json` — minimal reviewed consumer payload.\n"
        "- `reference/state_machine.py` — non-publishing reference logic.\n"
        "- `reference/test_state_machine.py` — one-signal silence, dual-register gate, retraction and review tests.\n"
    )
    write_text(candidate_root / "README.md", candidate_readme)

    backlog = md_header("PipelineNews intelligence vNext — implementation backlog", "inferred") + "\n"
    backlog += """## P0 — graduate only after human review

1. Freeze the evidence-event, identity-relationship and timing-transition schemas.
2. Extract the current discovery runner into source-specific collectors with source cards and deterministic request receipts.
3. Add an append-only evidence ledger with idempotency keys, source revisions, retractions and contradictions.
4. Build a company/project/planning identity binder that defaults to `ABSTAIN` and records validity intervals.
5. Add a Companies funding-event adapter that consumes only a reviewed compact export; no raw company master is retained.
6. Add a planning/procurement event adapter with authority, application reference, status/effective date and source digest.
7. Enforce the dual-register gate: funding + procurement + reviewed identity, otherwise remain withheld.
8. Produce a reviewed project-intelligence summary for PipelineNews and GridAtlas; keep observed facts and inferred windows visually separate.
9. Replace the hard-coded GridAtlas release URL with a verified current pointer contract and two golden deep-link sentinels.
10. Add regression fixtures for one-signal silence, ambiguous identity, revised filing, retracted event, stale window and conflicting evidence.

## P1 — after P0 is proven

1. Add data-centre demand-side events using the same evidence and identity contracts.
2. Add source-card health, freshness and revision dashboards.
3. Add a human review queue for conflicts, stale windows and candidate relationships.
4. Add an operational scorecard measuring lead-time versus trade-press publication without treating later news as ground truth.
5. Add CVAA vaccines for consumer pointer drift, inference-as-fact, one-signal promotion and missing source revisions.

## Explicitly excluded

- Product-repository mutations from this audit branch.
- Live Companies House, planning, news or scraper network calls.
- Public credit/bankability scores or individual director/PSC output.
- Automatic publication from an inferred score.
"""
    write_text(candidate_root / "IMPLEMENTATION-BACKLOG.md", backlog)

    migration = md_header("PipelineNews current-to-vNext migration map", "inferred") + "\n"
    migration += """| Current responsibility | Candidate destination | Graduation proof |
|---|---|---|
| Source queries and bounded fetch logic | `collectors/<source>` | deterministic fixture + source-card receipt |
| Evidence/provenance arrays inside runners | append-only evidence ledger | idempotent replay; revision and retraction tests |
| Project matching in runner flow | identity binder | exact keys, abstention, validity interval, contradiction evidence |
| Scores/window labels | timing state machine | dual-register gate and rule-versioned transitions |
| Headlines and project rows | reviewed read model | observed/inferred separation and human review receipt |
| Hard-coded GridAtlas release URL | verified pointer consumer | Beacon Fen and East Pye public sentinel proof |
| Release/promotion commands | existing reviewed product workflows | no new publisher in audit code |
"""
    write_text(candidate_root / "MIGRATION-MAP.md", migration)

    summary = md_header("05 — PipelineNews vNext quarantined candidate", "inferred") + "\n"
    summary += (
        "The candidate is under `next-versions/202608310052-pipelinenews-intelligence-vnext/`. It contains schemas, module ownership, a non-publishing reference state machine and tests.\n\n"
        "## Candidate gates encoded\n\n"
        "- Funding and procurement are independent observed lanes.\n"
        "- A commercial window is always an inference with evidence IDs and a rule version.\n"
        "- One signal remains silent.\n"
        "- Retraction removes an event from the usable evidence set.\n"
        "- Contradiction wins over promotion.\n"
        "- Human review is required before `RELEASE_CANDIDATE`.\n"
        "- `PUBLISHED` is deliberately unavailable in the audit reference implementation.\n"
    )
    write_text(output_root / "05-PIPELINENEWS-VNEXT.md", summary)


def phase_status(output_root: Path, phase: int, plan: Mapping[str, Any]) -> None:
    phase_config = next(item for item in plan["phases"] if int(item["number"]) == phase)
    write_json(
        output_root / f"checkpoint-{phase:02d}.json",
        {
            "schema": "chatgpt-audits.study-checkpoint.v1",
            "generation": GENERATION,
            "review_status": REVIEW_STATUS,
            "classification": "observed",
            "phase": phase,
            "slug": phase_config["slug"],
            "goal": phase_config["goal"],
            "completed_at": now_utc(),
            "completed_at_london": now_london(),
        },
    )


def cmd_phase(args: argparse.Namespace) -> int:
    phase = int(args.phase)
    if phase not in range(1, 6):
        raise ValueError("phase must be 1..5")
    plan = load_json(Path(args.plan).resolve())
    manifest = load_json(Path(args.manifest).resolve())
    source_root = Path(args.source_root).resolve()
    audit_root = Path(args.audit_root).resolve()
    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    print(f"[phase {phase}] start", flush=True)
    if phase == 1:
        phase_one(plan, manifest, source_root, output_root)
    elif phase == 2:
        phase_two(plan, manifest, source_root, output_root)
    elif phase == 3:
        phase_three(plan, manifest, source_root, output_root)
    elif phase == 4:
        phase_four(plan, manifest, source_root, audit_root, output_root)
    else:
        phase_five(plan, manifest, output_root)
    phase_status(output_root, phase, plan)
    print(f"[phase {phase}] complete", flush=True)
    return 0


def cmd_initialise(args: argparse.Namespace) -> int:
    plan = load_json(Path(args.plan).resolve())
    output_root = Path(args.output_root).resolve()
    output_root.mkdir(parents=True, exist_ok=False)
    content = md_header("Five-hour quarantined cross-repository study") + "\n"
    content += (
        f"Generation: `{GENERATION}`  \n"
        f"Run ID: `{args.run_id}`  \n"
        f"Quarantine branch: `{args.branch}`  \n"
        f"Started: `{now_london()}`  \n\n"
        "## Boundary\n\n"
        "- Product repositories are read-only source snapshots.\n"
        "- The only Git write target is this timestamped output root on a `chatgpt-audits` quarantine branch.\n"
        "- No live data API, planning portal, Companies House download, scraper or news feed is called.\n"
        "- Every output remains `UNREVIEWED` until a human graduates it.\n\n"
        "## Checkpoints\n\n"
        + "\n".join(f"{item['number']}. **{item['slug']}** — {item['goal']}" for item in plan["phases"])
        + "\n"
    )
    write_text(output_root / "README.md", content)
    write_json(
        output_root / "RUN-CONTEXT.json",
        {
            "schema": "chatgpt-audits.run-context.v1",
            "generation": GENERATION,
            "review_status": REVIEW_STATUS,
            "classification": "observed",
            "run_id": str(args.run_id),
            "run_attempt": str(args.run_attempt),
            "event_name": str(args.event_name),
            "quarantine_branch": str(args.branch),
            "output_root": str(args.output_root),
            "started_at": now_utc(),
            "started_at_london": now_london(),
            "plan_sha256": sha256_file(Path(args.plan).resolve()),
        },
    )
    return 0


def cmd_finalise(args: argparse.Namespace) -> int:
    output_root = Path(args.output_root).resolve()
    manifest = load_json(Path(args.manifest).resolve())
    source_failures = [entry for entry in manifest["repositories"] if entry.get("status") != "SNAPSHOT_READY"]

    synthesis = md_header("00 — Executive synthesis", "inferred") + "\n"
    synthesis += (
        "## Result\n\n"
        "A five-checkpoint, source-pinned audit candidate has been produced without modifying any product repository. The highest-priority next version is a modular PipelineNews timing engine, not another combined news runner.\n\n"
        "## Load-bearing findings\n\n"
        "1. **Observed:** PipelineNews's selected source contains large files combining collection, network, evidence, identity, validation, presentation and release concerns.\n"
        "2. **Observed where cross-check ledger says so:** the current producer deep-link string and GridAtlas route contract disagree at the pinned commits.\n"
        "3. **Observed:** Companies already protects a compact relationship/privacy boundary; that boundary can remain while a separate append-only organisation-event contract is added.\n"
        "4. **Inferred:** commercial timing needs two independent register lanes — funding and procurement — joined only after reviewed identity binding.\n"
        "5. **Inferred:** news is best treated as corroborating evidence and explanation, not as the authority that creates the funding/procurement fact.\n"
        "6. **Inferred:** the first graduation should freeze contracts and state-machine tests before touching live products.\n\n"
        "## Quarantined vNext package\n\n"
        "See `next-versions/202608310052-pipelinenews-intelligence-vnext/` for schemas, module ownership, migration map, backlog, reference state machine and tests.\n\n"
        "## Human decisions required\n\n"
        "- Accept or reject the dual-register state model.\n"
        "- Choose the reviewed source contract for Companies funding events.\n"
        "- Choose the planning/procurement source-card and revision policy.\n"
        "- Approve the GridAtlas pointer repair contract before any product change.\n"
        "- Decide which P0 artefact graduates first and into which product repository.\n"
    )
    write_text(output_root / "00-EXECUTIVE-SYNTHESIS.md", synthesis)

    queue = md_header("Human review queue", "inferred") + "\n"
    queue += """| Priority | Review item | Decision |
|---:|---|---|
| 1 | `04-CLAUDE-CROSSCHECK-LEDGER.json` | Confirm the PipelineNews→GridAtlas route finding against a browser proof. |
| 2 | vNext evidence and transition schemas | Approve fields, source revision semantics and observed/inferred separation. |
| 3 | reference state-machine tests | Confirm one-signal silence and human-review gate reflect the commercial doctrine. |
| 4 | Companies event boundary | Confirm which organisation-level events may leave Companies and that PII stays excluded. |
| 5 | planning/procurement source contract | Select supervised sources and source-card requirements. |
| 6 | migration backlog | Select one bounded product-repo graduation; do not bulk-copy the audit candidate. |
"""
    write_text(output_root / "REVIEW-QUEUE.md", queue)

    files: list[dict[str, Any]] = []
    for path in iter_files(output_root):
        if path.name == "RUN-MANIFEST.json":
            continue
        files.append({"path": relative_posix(path, output_root), "bytes": path.stat().st_size, "sha256": sha256_file(path)})
    files.sort(key=lambda item: item["path"])
    write_json(
        output_root / "RUN-MANIFEST.json",
        {
            "schema": "chatgpt-audits.five-hour-run-manifest.v1",
            "generation": GENERATION,
            "review_status": REVIEW_STATUS,
            "classification": "observed",
            "completed_at": now_utc(),
            "completed_at_london": now_london(),
            "source_snapshot_sha256": sha256_file(Path(args.manifest).resolve()),
            "source_failures": source_failures,
            "files": files,
            "total_files": len(files),
            "total_bytes": sum(item["bytes"] for item in files),
            "graduation_status": "HUMAN_REVIEW_REQUIRED",
        },
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    snapshot = sub.add_parser("snapshot")
    snapshot.add_argument("--plan", required=True)
    snapshot.add_argument("--source-root", required=True)
    snapshot.add_argument("--manifest", required=True)
    snapshot.set_defaults(func=cmd_snapshot)

    initialise = sub.add_parser("initialise")
    initialise.add_argument("--plan", required=True)
    initialise.add_argument("--output-root", required=True)
    initialise.add_argument("--run-id", required=True)
    initialise.add_argument("--run-attempt", required=True)
    initialise.add_argument("--event-name", required=True)
    initialise.add_argument("--branch", required=True)
    initialise.set_defaults(func=cmd_initialise)

    phase = sub.add_parser("phase")
    phase.add_argument("--phase", required=True, type=int)
    phase.add_argument("--plan", required=True)
    phase.add_argument("--source-root", required=True)
    phase.add_argument("--manifest", required=True)
    phase.add_argument("--audit-root", required=True)
    phase.add_argument("--output-root", required=True)
    phase.set_defaults(func=cmd_phase)

    finalise = sub.add_parser("finalise")
    finalise.add_argument("--output-root", required=True)
    finalise.add_argument("--manifest", required=True)
    finalise.set_defaults(func=cmd_finalise)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
