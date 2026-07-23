"""Convert contextual motion concepts into a Motion Studio production handoff."""

from __future__ import annotations

import re

from .models import AssetType, MarketingTask
from .motion_brief_engine import build_motion_brief


def build_motion_handoff(request: MarketingTask | str) -> dict[str, object]:
    task = _as_task(request)
    brief = build_motion_brief(task)
    slug = _slug(task.topic)
    scenes = [
        {
            **scene,
            "duration": f"{scene['start_seconds']}-{scene['end_seconds']}s",
        }
        for scene in brief["scenes"]
    ]
    return {
        "format": "motion studio production handoff",
        "target_workspace": "motion-studio",
        "required_skill": ".claude/skills/produce-motion-video/SKILL.md",
        "approval_status": "human_concept_approval_required",
        "render_manifest": {
            "slug": slug,
            "duration_seconds": 42,
            "aspect_ratios": ["9:16", "1:1", "16:9"],
            "language": task.language,
            "market": task.market,
            "style": brief["motion_language"],
            "output": f"export-video/{slug}.mp4",
        },
        "creative_brief": brief,
        "scenes": scenes,
        "qa_checks": [
            "Concept and storyboard receive human approval before scene implementation.",
            "Scene lint, orthography, deterministic timing, safe zones, and no-CDN rules pass.",
            "Product states use real or clearly labeled illustrative data.",
            "No claim implies guaranteed interviews, jobs, or universal ATS behavior.",
            "Contact sheet and final MP4 receive visual and technical review.",
        ],
        "source_request": task.request,
    }


def _as_task(value: MarketingTask | str) -> MarketingTask:
    if isinstance(value, MarketingTask):
        if value.asset_type not in {AssetType.MOTION_VIDEO, AssetType.MOTION_HANDOFF}:
            from dataclasses import replace

            return replace(value, asset_type=AssetType.MOTION_VIDEO)
        return value
    from .router import classify

    task = classify(value)
    if task.asset_type not in {AssetType.MOTION_VIDEO, AssetType.MOTION_HANDOFF}:
        from dataclasses import replace

        task = replace(task, asset_type=AssetType.MOTION_VIDEO)
    return task


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:64] or "worqai-motion"
