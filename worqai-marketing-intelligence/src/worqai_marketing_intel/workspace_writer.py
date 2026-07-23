"""Write approved capability source artifacts into target workspaces."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .artifact_writer import render_brief
from .models import ProductionResult, WorkspaceActionPlan


_ADAPTER_FORMATS = {
    "markdown": {"markdown"},
    "nextjs_implementation": {"implementation_brief_json"},
    "launch_content_archive": {"launch_content_markdown"},
    "carousel_build_export": {"carousel_spec_json"},
    "marketing_content_archive": {"marketing_brief_json"},
    "reel_factory_handoff": {"reel_factory_brief_json"},
    "produce_motion_video": {"motion_creative_brief_markdown"},
}

_FORMAT_SUFFIXES = {
    "markdown": ".md",
    "implementation_brief_json": ".json",
    "launch_content_markdown": ".md",
    "carousel_spec_json": ".json",
    "marketing_brief_json": ".json",
    "reel_factory_brief_json": ".json",
    "motion_creative_brief_markdown": ".md",
}


class WorkspaceWriter:
    def write_payload(
        self,
        *,
        plan_id: str,
        plan: WorkspaceActionPlan,
        brief_payload: dict[str, Any],
        dry_run: bool = True,
    ) -> ProductionResult:
        workspace = Path(plan.workspace_path).resolve()
        destination = (workspace / plan.asset_relative_path).resolve()
        notes: list[str] = []

        _validate_adapter(plan)
        if not _inside(destination, workspace):
            raise ValueError("Refusing to write outside the target workspace")
        if destination.suffix.lower() != _FORMAT_SUFFIXES[plan.source_format]:
            raise ValueError(
                f"Source format {plan.source_format} requires "
                f"a {_FORMAT_SUFFIXES[plan.source_format]} destination"
            )
        if not plan.can_write:
            notes.append("Plan is marked can_write=false; no file was written.")
            return _result(plan_id, plan, destination, dry_run, False, notes)
        if not workspace.is_dir():
            notes.append("Target workspace is not an accessible directory; no file was written.")
            return _result(plan_id, plan, destination, dry_run, False, notes)
        if dry_run:
            notes.append("Dry run only; no file was written.")
            notes.append(
                f"Would stage {plan.source_format} for capability {plan.capability_id}."
            )
            return _result(plan_id, plan, destination, True, False, notes)

        content = _render_source(plan, brief_payload, plan_id)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not _inside(destination.parent.resolve(), workspace):
            raise ValueError("Refusing to create a parent outside the target workspace")
        destination.write_text(content, encoding="utf-8")
        notes.append(
            f"Staged {plan.source_format} for {plan.capability_id}; "
            f"intended final output is {plan.output_format}."
        )
        return _result(plan_id, plan, destination, False, True, notes)


def plan_from_payload(payload: dict[str, Any]) -> WorkspaceActionPlan:
    return WorkspaceActionPlan(
        workspace_id=str(payload["workspace_id"]),
        workspace_path=str(payload["workspace_path"]),
        asset_type=str(payload["asset_type"]),
        source_request=str(payload["source_request"]),
        current_branch=payload.get("current_branch"),
        dirty=payload.get("dirty"),
        recommended_branch=str(payload["recommended_branch"]),
        asset_relative_path=str(payload["asset_relative_path"]),
        write_mode=str(payload["write_mode"]),
        can_write=bool(payload["can_write"]),
        human_approval_required=bool(payload["human_approval_required"]),
        verification_commands=tuple(payload.get("verification_commands", ())),
        safety_notes=tuple(payload.get("safety_notes", ())),
        capability_id=str(payload.get("capability_id", "legacy-markdown-brief")),
        adapter=str(payload.get("adapter", "markdown")),
        source_format=str(payload.get("source_format", "markdown")),
        output_format=str(payload.get("output_format", "markdown")),
    )


def _validate_adapter(plan: WorkspaceActionPlan) -> None:
    formats = _ADAPTER_FORMATS.get(plan.adapter)
    if formats is None:
        raise ValueError(f"Unsupported production adapter: {plan.adapter}")
    if plan.source_format not in formats:
        raise ValueError(
            f"Adapter {plan.adapter} does not accept source format {plan.source_format}"
        )
    if plan.source_format not in _FORMAT_SUFFIXES:
        raise ValueError(f"Unsupported source format: {plan.source_format}")


def _render_source(
    plan: WorkspaceActionPlan,
    brief_payload: dict[str, Any],
    plan_id: str,
) -> str:
    if plan.adapter == "carousel_build_export":
        return _json_text(_carousel_spec(brief_payload, plan_id))
    if plan.adapter == "nextjs_implementation":
        return _json_text(
            {
                "schema": "worqai.nextjs-implementation-brief/v1",
                "plan_id": plan_id,
                "capability": plan.capability_id,
                "source_request": plan.source_request,
                "intended_output": plan.output_format,
                "brief": brief_payload,
            }
        )
    if plan.adapter == "marketing_content_archive":
        return _json_text(
            {
                "schema": "worqai.marketing-production-brief/v1",
                "plan_id": plan_id,
                "capability": plan.capability_id,
                "asset_type": plan.asset_type,
                "intended_output": plan.output_format,
                "brief": brief_payload,
            }
        )
    if plan.adapter == "reel_factory_handoff":
        return _json_text(_reel_factory_brief(plan, brief_payload, plan_id))
    if plan.adapter == "produce_motion_video":
        return _motion_brief(plan, brief_payload, plan_id)
    return render_brief(brief_payload, record_id=plan_id)


def _reel_factory_brief(
    plan: WorkspaceActionPlan,
    brief: dict[str, Any],
    plan_id: str,
) -> dict[str, Any]:
    """Stage creative intent without pretending that clips or captions are approved."""
    return {
        "schema": "worqai.reel-factory-production-brief/v1",
        "plan_id": plan_id,
        "capability": plan.capability_id,
        "status": "requires_human_clip_caption_and_storyboard_review",
        "source_request": plan.source_request,
        "intended_output": plan.output_format,
        "brief": brief,
        "production_contract": {
            "real_footage_only": True,
            "synthetic_people_allowed": False,
            "machine_transcript_is_final": False,
            "reviewed_caption_corrections_required": True,
            "explicit_ordered_storyboard_required": True,
            "duration_or_topic_tags_prove_continuity": False,
            "automatic_posting_allowed": False,
            "full_candidate_watch_required": True,
            "hash_bound_human_approval_required": True,
        },
        "factory_handoff": {
            "workflow": "CLAUDE.md",
            "operator_guide": "docs/operator-guide.md",
            "remotion_spec_contract": "remotion/specs/README.md",
            "approved_release_source": "out/release-candidates/",
            "remotion_candidate_source": "out/remotion-candidates/",
            "rejected_legacy_source": "out/variants/",
            "next_step": (
                "A human reviews real manifest clips and caption corrections, then "
                "creates or approves the explicit factory storyboard/spec before rendering."
            ),
        },
    }


def _carousel_spec(brief: dict[str, Any], plan_id: str) -> dict[str, Any]:
    task = brief.get("task", {})
    concept = brief.get("concept", {})
    raw_slides = concept.get("slides", [])
    if not isinstance(raw_slides, list) or not raw_slides:
        raw_slides = [concept.get("recommended_hook", task.get("topic", "WorqAI"))]
    slides: list[dict[str, Any]] = []
    for index, raw_slide in enumerate(raw_slides, start=1):
        if isinstance(raw_slide, dict):
            headline = str(
                raw_slide.get("headline")
                or raw_slide.get("title")
                or raw_slide.get("copy")
                or raw_slide
            )
            body = str(raw_slide.get("body") or raw_slide.get("visual") or "")
            role = str(raw_slide.get("role", "explain"))
        else:
            headline = str(raw_slide)
            body = ""
            role = "hook" if index == 1 else "explain"
        slides.append(
            {
                "id": f"s{index}",
                "layout": "slide-hook-lockup" if role in {"hook", "cta"} else "slide-editorial-proof",
                "copy": {
                    "kicker": f"WORQAI / {index:02d}",
                    "headline": headline,
                    "body": body,
                },
            }
        )
    return {
        "meta": {
            "title": str(task.get("topic", "WorqAI carousel")),
            "topic": _topic_slug(str(task.get("topic", "worqai"))),
            "brand": "WorqAI",
            "system": "s17",
            "aspect": "1:1",
            "slides": len(slides),
            "language": str(task.get("language", "en")),
            "source_plan_id": plan_id,
        },
        "pacing": ["hook", *(["explain"] * max(0, len(slides) - 2)), "cta"]
        if len(slides) > 1
        else ["hook"],
        "slides": slides,
    }


def _motion_brief(
    plan: WorkspaceActionPlan,
    brief: dict[str, Any],
    plan_id: str,
) -> str:
    task = brief.get("task", {})
    concept = brief.get("concept", {})
    scenes = concept.get("scenes", [])
    scene_lines = "\n".join(
        _motion_scene_line(index, scene)
        for index, scene in enumerate(scenes, 1)
    )
    return (
        f"# Motion Production Brief\n\n"
        f"Plan ID: {plan_id}\n\n"
        f"## Objective\n{task.get('objective', 'awareness')}\n\n"
        f"## Audience\n{task.get('audience', '')}\n\n"
        f"## Offer\n{task.get('offer', 'WorqAI')}\n\n"
        f"## Platform And Format\n{task.get('channel') or 'social'}; "
        f"{concept.get('format', 'motion video')}\n\n"
        f"## Language\n{task.get('language', 'en')}\n\n"
        f"## Concept\n{concept.get('concept', plan.source_request)}\n\n"
        f"## Scenes\n{scene_lines or '- Define during approved storyboard stage.'}\n\n"
        f"## Motion Language\n{concept.get('motion_language', '')}\n\n"
        f"## Voiceover\n{concept.get('voiceover', '')}\n\n"
        f"## Call To Action\n{concept.get('cta', '')}\n\n"
        "## Production Contract\n"
        "Follow .claude/skills/produce-motion-video/SKILL.md and stop at every human gate.\n"
    )


def _json_text(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, ensure_ascii=True) + "\n"


def _motion_scene_line(index: int, scene: object) -> str:
    if not isinstance(scene, dict):
        return f"{index}. {scene}"
    timing = scene.get("duration") or (
        f"{scene.get('start_seconds', '?')}-{scene.get('end_seconds', '?')}s"
    )
    purpose = scene.get("purpose", "scene")
    visual = scene.get("visual", "")
    copy = scene.get("copy", "")
    return f"{index}. [{timing}] {purpose}: {visual} Copy: {copy}"


def _topic_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:64].strip("-") or "worqai"


def _result(
    plan_id: str,
    plan: WorkspaceActionPlan,
    destination: Path,
    dry_run: bool,
    wrote: bool,
    notes: list[str],
) -> ProductionResult:
    return ProductionResult(
        plan_id=plan_id,
        workspace_id=plan.workspace_id,
        destination_path=str(destination),
        dry_run=dry_run,
        wrote=wrote,
        verification_commands=plan.verification_commands,
        notes=tuple(notes),
    )


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True
