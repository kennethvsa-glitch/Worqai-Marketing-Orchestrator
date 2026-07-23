#!/usr/bin/env python3
"""Hash-bound production jobs for standalone carousel slide approval."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
JOBS = ROOT / ".creative-production" / "jobs"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def job_path(job_id: str) -> Path:
    path = JOBS / job_id / "job.json"
    if not path.is_file():
        raise ValueError(f"unknown job: {job_id}")
    return path


def artifact_hash(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        resolved = path.expanduser().resolve()
        if not resolved.is_file():
            raise ValueError(f"artifact does not exist: {resolved}")
        digest.update(resolved.name.encode())
        digest.update(b"\0")
        digest.update(resolved.read_bytes())
    return digest.hexdigest()


def create(args: argparse.Namespace) -> dict:
    brief = args.brief.expanduser().resolve()
    if not brief.is_file():
        raise ValueError(f"brief does not exist: {brief}")
    job_id = uuid4().hex
    job = {
        "id": job_id,
        "status": "concept_review",
        "created_at": now(),
        "updated_at": now(),
        "brief": str(brief),
        "brief_hash": artifact_hash([brief]),
        "art_direction": None,
        "concept_approval": None,
        "slides": {},
        "assembled": None,
        "final_approval": None,
    }
    write(JOBS / job_id / "job.json", job)
    return job


def approve_concept(args: argparse.Namespace) -> dict:
    path = job_path(args.job_id)
    job = read(path)
    contract = args.contract.expanduser().resolve()
    digest = artifact_hash([contract])
    job["art_direction"] = {"path": str(contract), "hash": digest}
    job["concept_approval"] = {"hash": digest, "approved_at": now(), "by": args.by}
    job["status"] = "producing_slides"
    job["updated_at"] = now()
    write(path, job)
    return job


def submit_slide(args: argparse.Namespace) -> dict:
    path = job_path(args.job_id)
    job = read(path)
    files = [item.expanduser().resolve() for item in (args.html, args.render, args.report)]
    digest = artifact_hash(files)
    job["slides"][args.slide_id] = {
        "html": str(files[0]), "render": str(files[1]), "report": str(files[2]),
        "hash": digest, "submitted_at": now(), "approval": None,
    }
    job["status"] = "slide_review"
    job["updated_at"] = now()
    write(path, job)
    return job


def approve_slide(args: argparse.Namespace) -> dict:
    path = job_path(args.job_id)
    job = read(path)
    slide = job["slides"].get(args.slide_id)
    if slide is None:
        raise ValueError(f"unknown slide: {args.slide_id}")
    current = artifact_hash([Path(slide[key]) for key in ("html", "render", "report")])
    if current != slide["hash"]:
        raise ValueError("slide changed after submission; submit it again")
    slide["approval"] = {"hash": current, "approved_at": now(), "by": args.by}
    job["updated_at"] = now()
    write(path, job)
    return job


def ready(args: argparse.Namespace) -> dict:
    job = read(job_path(args.job_id))
    if not job["concept_approval"]:
        raise ValueError("concept approval is missing")
    if not job["slides"]:
        raise ValueError("no slides submitted")
    for slide_id, slide in job["slides"].items():
        current = artifact_hash([Path(slide[key]) for key in ("html", "render", "report")])
        if not slide["approval"] or slide["approval"]["hash"] != current:
            raise ValueError(f"slide {slide_id} is unapproved or changed")
    return {"job_id": job["id"], "ready": True, "approved_slides": sorted(job["slides"])}


def show(args: argparse.Namespace) -> dict:
    return read(job_path(args.job_id))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    new = commands.add_parser("new"); new.add_argument("brief", type=Path); new.set_defaults(handler=create)
    concept = commands.add_parser("approve-concept"); concept.add_argument("job_id"); concept.add_argument("contract", type=Path); concept.add_argument("--by", default="human"); concept.set_defaults(handler=approve_concept)
    submit = commands.add_parser("submit-slide"); submit.add_argument("job_id"); submit.add_argument("slide_id"); submit.add_argument("html", type=Path); submit.add_argument("render", type=Path); submit.add_argument("report", type=Path); submit.set_defaults(handler=submit_slide)
    approve = commands.add_parser("approve-slide"); approve.add_argument("job_id"); approve.add_argument("slide_id"); approve.add_argument("--by", default="human"); approve.set_defaults(handler=approve_slide)
    check = commands.add_parser("ready"); check.add_argument("job_id"); check.set_defaults(handler=ready)
    status = commands.add_parser("status"); status.add_argument("job_id"); status.set_defaults(handler=show)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        result = args.handler(args)
    except (KeyError, ValueError) as error:
        print(json.dumps({"ok": False, "error": str(error)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
