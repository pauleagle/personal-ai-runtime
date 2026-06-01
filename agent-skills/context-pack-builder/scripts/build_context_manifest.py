#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return sum(1 for _line in handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_source(repo_root: Path, source: str, max_bytes: int) -> dict[str, Any]:
    raw_path = Path(source)
    path = raw_path if raw_path.is_absolute() else repo_root / raw_path
    normalized = path.resolve()
    item: dict[str, Any] = {
        "input": source,
        "path": str(normalized),
        "relativePath": None,
        "exists": normalized.exists(),
        "kind": "missing",
        "warnings": [],
    }

    try:
        item["relativePath"] = normalized.relative_to(repo_root).as_posix()
    except ValueError:
        item["warnings"].append("outside-repo-root")

    if not normalized.exists():
        item["warnings"].append("missing")
        return item

    if normalized.is_dir():
        item["kind"] = "directory"
        item["warnings"].append("directory-not-file")
        return item

    if not normalized.is_file():
        item["kind"] = "other"
        item["warnings"].append("not-regular-file")
        return item

    size = normalized.stat().st_size
    item.update(
        {
            "kind": "file",
            "bytes": size,
            "lines": count_lines(normalized),
            "sha256": sha256_file(normalized),
        }
    )

    if size > max_bytes:
        item["warnings"].append("exceeds-max-bytes")

    return item


def build_manifest(repo_root: Path, sources: list[str], max_bytes: int) -> dict[str, Any]:
    repo_root = repo_root.resolve()

    if not repo_root.exists():
        return {"valid": False, "message": f"Repository path does not exist: {repo_root}"}
    if not repo_root.is_dir():
        return {"valid": False, "message": f"Repository path is not a directory: {repo_root}"}

    inspected = [inspect_source(repo_root, source, max_bytes) for source in sources]
    total_bytes = sum(item.get("bytes", 0) for item in inspected)
    warnings = [
        {"source": item["input"], "warnings": item["warnings"]}
        for item in inspected
        if item["warnings"]
    ]

    return {
        "valid": not any("missing" in item["warnings"] for item in inspected),
        "message": "Context manifest built.",
        "repoRoot": str(repo_root),
        "sourceCount": len(inspected),
        "fileCount": sum(1 for item in inspected if item["kind"] == "file"),
        "totalBytes": total_bytes,
        "maxBytesPerFile": max_bytes,
        "sources": inspected,
        "warnings": warnings,
    }


def emit_markdown(result: dict[str, Any]) -> None:
    print(f"Repository: {result.get('repoRoot', '(unknown)')}")
    print(f"Sources: {result.get('sourceCount', 0)}")
    print(f"Files: {result.get('fileCount', 0)}")
    print(f"Total bytes: {result.get('totalBytes', 0)}")
    print()
    print("### Sources")
    print()

    for item in result.get("sources", []):
        marker = ", ".join(item["warnings"]) if item["warnings"] else "ok"
        print(f"- {item['input']}: {item['kind']} ({marker})")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build deterministic source metadata for a bounded context pack."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-bytes", type=int, default=200_000)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("sources", nargs="+")
    args = parser.parse_args(argv)

    result = build_manifest(Path(args.repo_root), args.sources, args.max_bytes)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result.get("valid"):
        emit_markdown(result)
    else:
        print(result["message"], file=sys.stderr)
        if result.get("sources"):
            emit_markdown(result)

    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
