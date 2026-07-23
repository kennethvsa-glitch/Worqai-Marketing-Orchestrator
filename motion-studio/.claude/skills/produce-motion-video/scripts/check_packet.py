#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path


REQUIRED_GATES = {"creative-spec", "storyboard", "scene-taste", "assembly-taste", "human-review"}
REQUIRED_ROLES = {"creative-director", "taste-director", "motion-scene-engineer", "visual-verifier", "media-verifier"}


def validate(packet: dict) -> list[str]:
    errors: list[str] = []
    if not str(packet.get("brief", "")).strip():
        errors.append("brief is empty")
    dag = packet.get("dag")
    if not isinstance(dag, list) or not dag:
        errors.append("dag is empty")
        return errors
    ids = [task.get("id") for task in dag]
    if len(ids) != len(set(ids)):
        errors.append("dag task ids are not unique")
    roles = {task.get("role") for task in dag}
    missing_roles = REQUIRED_ROLES - roles
    if missing_roles:
        errors.append("missing roles: " + ", ".join(sorted(missing_roles)))
    gates = set(packet.get("approval_gates", []))
    missing_gates = REQUIRED_GATES - gates
    if missing_gates:
        errors.append("missing approval gates: " + ", ".join(sorted(missing_gates)))
    for key in ("taste_policy", "visual_language_schema", "taste_finding_schema"):
        if not packet.get(key): errors.append(f"missing contract reference: {key}")
    known: set[str] = set()
    for task in dag:
        unknown = set(task.get("depends_on", [])) - known
        if unknown:
            errors.append(f"{task.get('id')} has unknown or forward dependencies: {sorted(unknown)}")
        known.add(task.get("id"))
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    packet = json.loads(args.packet.read_text(encoding="utf-8"))
    errors = validate(packet)
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
