"""Infer one executable route for vague or unsupported WMI prompts."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from .models import AssetType
from .router import classify, has_phrase, normalize_text


ResultT = TypeVar("ResultT")


MODE_BY_ASSET = {
    AssetType.CAMPAIGN_PACKAGE: "campaign_package",
    AssetType.SEO_PAGE: "seo_plan",
    AssetType.DEEP_RESEARCH: "deep_research",
    AssetType.FEEDBACK_LOOP: "feedback_loop",
    AssetType.MOTION_HANDOFF: "motion_handoff",
    AssetType.MESSAGE_REPLY: "message_reply",
    AssetType.RESEARCH: "research",
}


def build_universal_intake(prompt: str) -> dict[str, object]:
    """Return a single route decision; the prompt runtime executes it once."""

    normalized = normalize_text(prompt)
    intent = _intent(normalized)
    best_mode, evidence = _best_mode(prompt, normalized, intent)
    return {
        "format": "universal marketing route decision",
        "interpreted_intent": intent,
        "best_mode": best_mode,
        "confidence": _confidence(normalized, evidence),
        "evidence": list(evidence),
        "execution_policy": "execute_once_with_recursion_guard",
        "source_request": prompt,
    }


def execute_universal_intake(
    prompt: str,
    dispatch: Callable[[str], ResultT],
) -> tuple[dict[str, object], ResultT]:
    """Infer one mode and invoke the guarded runtime dispatch exactly once."""

    decision = build_universal_intake(prompt)
    return decision, dispatch(str(decision["best_mode"]))


def _intent(text: str) -> str:
    if _any_phrase(text, ("what can you do", "what can wmi do", "how do i use", "que puedes hacer", "como uso")):
        return "capability_question"
    if _any_phrase(text, ("is this good", "feels weak", "weak", "cringe", "bad", "taste", "mejor", "se siente debil")):
        return "taste_or_quality_check"
    if _any_phrase(text, ("what should", "next", "prioritize", "missing", "roadmap", "que hacemos", "que sigue", "priorizar")):
        return "strategy_next_step"
    if _any_phrase(text, ("idea", "ideas", "angle", "hook", "content", "angulo", "gancho", "contenido")):
        return "idea_generation"
    if _any_phrase(text, ("write", "make", "create", "draft", "generate", "escribe", "haz", "crea", "redacta", "genera")):
        return "asset_creation"
    return "ambiguous_marketing_request"


def _best_mode(prompt: str, text: str, intent: str) -> tuple[str, tuple[str, ...]]:
    task = classify(prompt)
    if task.signals:
        mode = MODE_BY_ASSET.get(task.asset_type, "brief")
        return mode, task.signals

    if intent == "strategy_next_step":
        return "campaign_package", ("strategy_next_step",)
    if intent == "taste_or_quality_check":
        return "brief", ("taste_or_quality_check",)
    if intent in {"idea_generation", "asset_creation"}:
        return "brief", (intent,)
    if intent == "capability_question":
        return "brief", ("capability_question",)
    return "brief", ("marketing_default",)


def _confidence(text: str, evidence: tuple[str, ...]) -> float:
    if evidence and evidence != ("marketing_default",):
        return 0.76 if len(text.split()) >= 5 else 0.68
    return 0.52 if len(text.split()) >= 5 else 0.45


def _any_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    return any(has_phrase(text, phrase) for phrase in phrases)
