#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a gated Motion Studio production job")
    parser.add_argument("brief", type=Path)
    parser.add_argument("--duration", type=float)
    parser.add_argument("--lane", choices=("template", "narrative"), default="narrative")
    parser.add_argument("--aspect", default="9:16")
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()

    brief_path = args.brief.resolve()
    if not brief_path.is_file():
        raise SystemExit(f"Brief not found: {brief_path}")
    brief = brief_path.read_text(encoding="utf-8")
    job_id = uuid4().hex
    root = Path.cwd().resolve()
    job_dir = root / ".visual-production" / "jobs" / job_id
    job_dir.mkdir(parents=True, exist_ok=False)
    (job_dir / "evidence").mkdir()

    dag = [
        {"id": "creative-spec", "role": "creative-director", "depends_on": []},
        {"id": "concept-taste", "role": "taste-director", "depends_on": ["creative-spec"]},
        {"id": "visual-language", "role": "creative-director", "depends_on": ["concept-taste"]},
        {"id": "storyboard", "role": "storyboard-editor", "depends_on": ["visual-language"]},
        {"id": "storyboard-taste", "role": "taste-director", "depends_on": ["storyboard"]},
        {"id": "scene", "role": "motion-scene-engineer", "depends_on": ["storyboard-taste"]},
        {"id": "copy", "role": "copy-editor", "depends_on": ["storyboard-taste"]},
        {"id": "audio-plan", "role": "media-engineer", "depends_on": ["storyboard-taste"]},
        {"id": "draft", "role": "render-controller", "depends_on": ["scene", "copy", "audio-plan"]},
        {"id": "scene-taste", "role": "taste-director", "depends_on": ["draft"]},
        {"id": "visual-qa", "role": "visual-verifier", "depends_on": ["scene-taste"]},
        {"id": "technical-qa", "role": "media-verifier", "depends_on": ["draft"]},
        {"id": "assembly-taste", "role": "taste-director", "depends_on": ["visual-qa", "technical-qa"]},
        {"id": "human-review", "role": "human", "depends_on": ["assembly-taste"]},
    ]
    if args.lane == "template":
        dag = [task for task in dag if task["id"] != "audio-plan"]
        next(task for task in dag if task["id"] == "draft")["depends_on"].remove("audio-plan")

    settings = {
        "lane": args.lane,
        "duration_seconds": args.duration,
        "aspect": args.aspect,
        "fps": args.fps,
    }
    packet = {
        "job_id": job_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "brief_path": str(brief_path),
        "brief": brief,
        "settings": settings,
        "dag": dag,
        "approval_gates": ["creative-spec", "storyboard", "scene-taste", "assembly-taste", "human-review"],
        "taste_policy": "config/taste-policy.json",
        "visual_language_schema": "config/visual-language.schema.json",
        "taste_finding_schema": "config/taste-finding.schema.json",
        "input_sha256": hashlib.sha256(
            (brief + json.dumps(settings, sort_keys=True)).encode()
        ).hexdigest(),
    }
    output = job_dir / "production-packet.json"
    output.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    print(json.dumps({"job_id": job_id, "packet": str(output)}, indent=2))


if __name__ == "__main__":
    main()
