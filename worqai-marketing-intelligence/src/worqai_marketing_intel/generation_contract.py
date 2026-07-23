"""Shared contract between deterministic WMI context and creative reasoning."""

from __future__ import annotations

from .models import AgentInsight, AssetType, BenchmarkPattern, GenerationPacket, MarketingTask


REQUIREMENTS: dict[AssetType, tuple[str, ...]] = {
    AssetType.IG_REEL: (
        "Deliver distinct concepts, each with a sub-three-second hook, spoken script, visual beats, caption, and CTA.",
        "Keep one idea per concept and show the product mechanism before the CTA.",
    ),
    AssetType.CAROUSEL: (
        "Deliver a complete slide sequence with one job per slide, visual direction, caption, and CTA.",
        "Use a tension -> mechanism -> proof -> action progression.",
    ),
    AssetType.MOTION_VIDEO: (
        "Deliver timed scenes, voiceover, on-screen copy, transitions, sound intent, and mobile-safe framing.",
        "Every scene must be feasible in Motion Studio's HTML/CSS/SVG pipeline.",
    ),
    AssetType.PARTNERSHIP_PITCH: (
        "Name the stakeholder, their operational pain, the low-risk pilot, proof required, objections, and next meeting ask.",
        "Adapt the language to the named organization instead of emitting a universal pitch pack.",
    ),
    AssetType.MESSAGE_REPLY: (
        "Answer the exact concern in the source message before adding product context.",
        "Return one recommended reply plus a shorter alternative; do not turn it into a sales pitch.",
    ),
    AssetType.SEO_PAGE: (
        "Match one primary search intent with page title, H1, outline, proof, FAQ, internal links, schema, and CTA.",
        "Separate researched facts from hypotheses and implementation tasks.",
    ),
}


CLAIMS_TO_QUALIFY = (
    "All ATS systems behave the same way.",
    "A recruiter will definitely see an aligned CV.",
    "WorqAI guarantees interviews, jobs, rankings, or ATS passage.",
    "WorqAI invents missing experience or credentials.",
)


def build_generation_packet(
    task: MarketingTask,
    brand_context: dict[str, str],
    patterns: tuple[BenchmarkPattern, ...],
    insights: tuple[AgentInsight, ...],
) -> GenerationPacket:
    requirements = list(REQUIREMENTS.get(task.asset_type, (
        "Deliver a complete, channel-native asset with hook, mechanism, proof, and one next step.",
    )))
    requirements.extend(task.constraints)
    source_facts = tuple(str(item) for item in task.metadata.get("source_facts", ()))
    if source_facts:
        requirements.append("Preserve source facts and intent; repair wording without replacing the subject.")
    return GenerationPacket(
        task=task,
        brand_context=brand_context,
        benchmark_patterns=patterns,
        agent_insights=insights,
        requirements=tuple(requirements),
        claims_to_qualify=CLAIMS_TO_QUALIFY,
        source_facts=source_facts,
    )
