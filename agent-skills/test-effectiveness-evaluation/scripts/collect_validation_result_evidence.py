#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


MUTATION_TERMS = ("killed", "survived", "equivalent", "skipped", "blocked")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def parse_unittest_output(text: str) -> dict[str, Any]:
    evidence: dict[str, Any] = {"detected": False}
    match = re.search(r"Ran\s+(\d+)\s+tests?\s+in\s+([0-9.]+)s", text)

    if match:
        evidence.update(
            {
                "detected": True,
                "testsRun": int(match.group(1)),
                "seconds": float(match.group(2)),
            }
        )

    if re.search(r"\bOK\b", text):
        evidence["status"] = "passed"

    failed = re.search(r"FAILED\s+\((.*?)\)", text)
    if failed:
        evidence["status"] = "failed"
        details = failed.group(1)
        for key, value in re.findall(r"(failures|errors|skipped)=(\d+)", details):
            evidence[key] = int(value)

    return evidence


def parse_mutation_terms(text: str) -> dict[str, Any]:
    lowered = text.lower()
    counts = {}
    for term in MUTATION_TERMS:
        numeric_values = [
            int(value)
            for value in re.findall(rf"\b{re.escape(term)}\b\s*[:=]\s*(\d+)", lowered)
        ]
        counts[term] = sum(numeric_values) if numeric_values else len(
            re.findall(rf"\b{re.escape(term)}\b", lowered)
        )
    return {
        "detected": any(counts.values()),
        "termCounts": counts,
    }


def collect(paths: list[Path]) -> dict[str, Any]:
    sources = []

    for path in paths:
        item: dict[str, Any] = {
            "input": str(path),
            "path": str(path.resolve()),
            "exists": path.exists(),
            "warnings": [],
        }

        if not path.exists():
            item["warnings"].append("missing")
            sources.append(item)
            continue

        if not path.is_file():
            item["warnings"].append("not-file")
            sources.append(item)
            continue

        text = read_text(path)
        item.update(
            {
                "bytes": path.stat().st_size,
                "unittest": parse_unittest_output(text),
                "mutationTerms": parse_mutation_terms(text),
            }
        )
        sources.append(item)

    return {
        "valid": not any("missing" in item["warnings"] for item in sources),
        "message": "Validation result evidence collected.",
        "sources": sources,
    }


def emit_markdown(result: dict[str, Any]) -> None:
    print("### Validation Result Evidence")
    print()
    for source in result["sources"]:
        warnings = ", ".join(source["warnings"]) if source["warnings"] else "ok"
        print(f"- {source['input']}: {warnings}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract deterministic evidence from test or mutation result text files."
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("result_files", nargs="+")
    args = parser.parse_args(argv)

    result = collect([Path(path) for path in args.result_files])

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result.get("valid"):
        emit_markdown(result)
    else:
        print(result["message"], file=sys.stderr)
        emit_markdown(result)

    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
