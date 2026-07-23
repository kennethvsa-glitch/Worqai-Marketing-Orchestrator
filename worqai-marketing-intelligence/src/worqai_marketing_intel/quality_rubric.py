"""Asset-specific quality rubrics."""

from __future__ import annotations

from .models import AssetType


def asset_rubric(asset_type: AssetType | str, text: str) -> tuple[int, tuple[str, ...], tuple[str, ...]]:
    kind = AssetType(asset_type) if not isinstance(asset_type, AssetType) else asset_type
    lowered = text.lower()
    strengths: list[str] = []
    risks: list[str] = []
    penalty = 0

    if kind == AssetType.IG_REEL:
        penalty += _require_any(
            lowered,
            ("hook", "first three seconds", "3 seconds", "visuals", "beats"),
            "Reel includes hook/beat/visual structure.",
            "Reel needs explicit hook, beats, and visual direction.",
            strengths,
            risks,
        )
        penalty += _require_any(
            lowered,
            ("caption", "cta", "call to action"),
            "Reel includes caption or CTA.",
            "Reel needs a caption or CTA.",
            strengths,
            risks,
        )
    elif kind == AssetType.CAROUSEL:
        penalty += _require_any(
            lowered,
            ("slides", "slide", "hook_options", "recommended_hook"),
            "Carousel includes slide or hook structure.",
            "Carousel needs slide sequence and hook options.",
            strengths,
            risks,
        )
        penalty += _require_any(
            lowered,
            ("visual_direction", "visual", "caption"),
            "Carousel includes visual direction.",
            "Carousel needs stronger visual direction.",
            strengths,
            risks,
        )
    elif kind == AssetType.MOTION_VIDEO:
        penalty += _require_any(
            lowered,
            ("scenes", "scene", "voiceover", "motion_language"),
            "Motion brief includes scenes and motion language.",
            "Motion brief needs scenes, pacing, and motion language.",
            strengths,
            risks,
        )
    elif kind == AssetType.PARTNERSHIP_PITCH:
        penalty += _require_any(
            lowered,
            ("pilot", "target_segments", "objections", "proof_to_prepare"),
            "Pitch includes pilot, proof, and objections.",
            "Pitch needs pilot scope, proof, and objection handling.",
            strengths,
            risks,
        )
        penalty += _require_any(
            lowered,
            ("universities", "institutions", "companies", "career centers"),
            "Pitch names target stakeholder segments.",
            "Pitch needs explicit stakeholder segmentation.",
            strengths,
            risks,
        )
    elif kind == AssetType.SEO_PAGE:
        penalty += _require_any(
            lowered,
            ("keyword", "title", "h1", "schema", "internal_link"),
            "SEO plan includes keyword, metadata, schema, and internal-link signals.",
            "SEO plan needs keyword pages, metadata, schema, and internal links.",
            strengths,
            risks,
        )
    elif kind == AssetType.CAMPAIGN_PACKAGE:
        penalty += _require_any(
            lowered,
            ("reels", "carousel", "seo", "distribution_plan"),
            "Campaign package includes multi-channel assets and distribution.",
            "Campaign package needs multi-channel assets and a distribution plan.",
            strengths,
            risks,
        )
    elif kind == AssetType.MESSAGE_REPLY:
        penalty += _require_any(
            lowered,
            ("recommended_reply", "short_reply", "follow_up_question"),
            "Reply output includes response options and a follow-up.",
            "Reply output needs a recommended reply, short reply, and follow-up.",
            strengths,
            risks,
        )
    elif kind == AssetType.DEEP_RESEARCH:
        penalty += _require_any(
            lowered,
            ("source_sets", "pattern_matrix", "output_after_research"),
            "Research plan defines sources, extraction fields, and outputs.",
            "Research plan needs sources, extraction fields, and deliverables.",
            strengths,
            risks,
        )
    elif kind == AssetType.FEEDBACK_LOOP:
        penalty += _require_any(
            lowered,
            ("events_to_track", "metrics_by_channel", "weekly_review"),
            "Feedback loop defines events, metrics, and review cadence.",
            "Feedback loop needs tracked events, metrics, and review cadence.",
            strengths,
            risks,
        )
    return penalty, tuple(strengths), tuple(risks)


def _require_any(
    text: str,
    signals: tuple[str, ...],
    strength: str,
    risk: str,
    strengths: list[str],
    risks: list[str],
) -> int:
    if any(signal in text for signal in signals):
        strengths.append(strength)
        return 0
    risks.append(risk)
    return 1
