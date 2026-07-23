#!/usr/bin/env python3
"""Validate creative contracts and run cheap deterministic taste checks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DIMENSIONS = {"composition", "hierarchy", "typography", "restraint", "originality", "brand_fit", "storytelling"}
SEVERITIES = {"minor", "major", "blocking"}
CONTRACT_FIELDS = {"audience", "objective", "tone", "concept", "typography", "color_roles", "composition", "restraint", "continuity", "prohibited_patterns"}
FINDING_FIELDS = {"id", "artifact", "dimension", "severity", "evidence", "direction", "confidence", "judgment"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_contract(value: dict) -> list[str]:
    errors = [f"missing field: {name}" for name in sorted(CONTRACT_FIELDS - value.keys())]
    if not isinstance(value.get("tone"), list) or not value.get("tone"):
        errors.append("tone must be a non-empty list")
    for name in ("composition", "restraint", "continuity"):
        if not isinstance(value.get(name), list) or not value.get(name):
            errors.append(f"{name} must be a non-empty list")
    return errors


def validate_findings(values: list[dict]) -> list[str]:
    errors: list[str] = []
    for index, value in enumerate(values):
        prefix = f"finding[{index}]"
        for name in sorted(FINDING_FIELDS - value.keys()):
            errors.append(f"{prefix} missing field: {name}")
        if value.get("dimension") not in DIMENSIONS:
            errors.append(f"{prefix} invalid dimension")
        if value.get("severity") not in SEVERITIES:
            errors.append(f"{prefix} invalid severity")
        confidence = value.get("confidence")
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            errors.append(f"{prefix} confidence must be between 0 and 1")
    return errors


def inspect_html(path: Path) -> list[dict]:
    content = path.read_text(encoding="utf-8", errors="replace")
    findings: list[dict] = []
    checks = [
        (not re.search(r"--(?:accent|color-accent)\s*:", content, re.I), "brand_fit", "major", "No explicit accent token was found.", "Declare and use a contract-approved accent token."),
        (bool(re.search(r"font-family\s*:\s*['\"]?(Inter|Roboto)\b", content, re.I)), "originality", "minor", "A generic default typeface is hardcoded.", "Use the approved brand typography or document the deliberate exception."),
        (bool(re.search(r"linear-gradient\([^)]*(?:#?7c3aed|purple|violet)", content, re.I)), "originality", "major", "An unapproved purple gradient pattern was detected.", "Replace it with a concept-specific brand color treatment."),
        (content.lower().count("border-radius") > 12, "restraint", "minor", "Border radius is repeated extensively.", "Confirm every rounded container has a functional purpose and remove ornamental wrappers."),
    ]
    for index, (triggered, dimension, severity, evidence, direction) in enumerate(checks, 1):
        if triggered:
            findings.append({"id": f"det-{index}", "artifact": str(path), "dimension": dimension, "severity": severity, "evidence": evidence, "direction": direction, "confidence": 1.0, "judgment": "objective", "requires_human": False})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    contract = commands.add_parser("contract"); contract.add_argument("path", type=Path)
    findings = commands.add_parser("findings"); findings.add_argument("path", type=Path)
    inspect = commands.add_parser("inspect-html"); inspect.add_argument("path", type=Path); inspect.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.command == "contract":
        errors = validate_contract(load(args.path))
        result = {"valid": not errors, "errors": errors}
    elif args.command == "findings":
        errors = validate_findings(load(args.path))
        result = {"valid": not errors, "errors": errors}
    else:
        values = inspect_html(args.path)
        result = {"passed": not any(item["severity"] in {"major", "blocking"} for item in values), "findings": values}
        if args.output:
            args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result.get("valid", result.get("passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
