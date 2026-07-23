"""Two-tier validation: deterministic hard gates + a Claude judge packet.

Tier 1 (this module) is deterministic and cheap. It returns pass/fail gates with
reasons. Only brand-safety, claim-safety, language, and source-fidelity gates
*block*; format completeness is advisory, because a concise and correct asset can
legitimately omit a keyword the rubric looks for.

Tier 2 is the judge packet. WMI deliberately does not fabricate a numeric taste
score here. It hands the creative operator the draft, brand excerpts, and a
rubric to score against as a separate pass — citing exact sentences for every
deduction. This is where real quality judgment happens.
"""

from __future__ import annotations

from dataclasses import dataclass

from .brand_memory import BrandMemory
from .models import MarketingTask
from .quality_rubric import asset_rubric
from .text_signals import looks_spanish, preserves_source, risky_claims

BLOCK = "block"
WARN = "warn"


@dataclass(frozen=True)
class GateResult:
    id: str
    severity: str
    passed: bool
    detail: str


def evaluate_hard_gates(
    text: str, task: MarketingTask, brand: BrandMemory
) -> tuple[GateResult, ...]:
    """Run the deterministic gates for a draft against its task."""

    lowered = text.lower()
    results: list[GateResult] = []

    banned = tuple(phrase for phrase in brand.banned_phrases() if phrase in lowered)
    results.append(
        GateResult(
            "banned_phrases",
            BLOCK,
            not banned,
            "No banned anti-slop language."
            if not banned
            else "Remove banned generic phrases: " + ", ".join(banned),
        )
    )

    risky = risky_claims(text)
    results.append(
        GateResult(
            "absolute_claims",
            BLOCK,
            not risky,
            "No unqualified outcome or ATS guarantees."
            if not risky
            else "Qualify or remove absolute claims: " + ", ".join(risky),
        )
    )

    if task.language.lower().startswith("es"):
        spanish = looks_spanish(text)
        results.append(
            GateResult(
                "language_match",
                BLOCK,
                spanish,
                "Reads as Spanish/LatAm."
                if spanish
                else "Spanish output was requested but the draft is not clearly Spanish.",
            )
        )

    if task.source_text.strip():
        preserved = preserves_source(text, task.source_text)
        results.append(
            GateResult(
                "source_fidelity",
                BLOCK,
                preserved,
                "Preserves the supplied source material."
                if preserved
                else "The draft may have replaced rather than preserved the source idea.",
            )
        )

    penalty, _strengths, format_risks = asset_rubric(task.asset_type, text)
    results.append(
        GateResult(
            "format_completeness",
            WARN,
            penalty == 0,
            "Includes the structural elements expected for this asset type."
            if penalty == 0
            else " ".join(format_risks),
        )
    )

    return tuple(results)


def blocking_failures(gates: tuple[GateResult, ...]) -> tuple[GateResult, ...]:
    return tuple(gate for gate in gates if gate.severity == BLOCK and not gate.passed)


def gate_to_dict(gate: GateResult) -> dict[str, object]:
    return {
        "id": gate.id,
        "severity": gate.severity,
        "passed": gate.passed,
        "detail": gate.detail,
    }


JUDGE_RUBRIC: dict[str, dict[str, object]] = {
    "taste": {
        "intent": "Does it feel premium, specific, and professionally usable?",
        "questions": [
            "Does it read as specific and considered rather than generic or templated?",
            "Is there one sharp mechanism or idea instead of a pile of claims?",
            "Is the CTA proportionate to the relationship rather than pushy?",
        ],
    },
    "fidelity": {
        "intent": "Is it true to the request, the source, and the product?",
        "questions": [
            "Does it actually address the requested topic and audience?",
            "If source text was supplied, is its strongest idea preserved rather than replaced?",
            "Are all product and ATS claims qualified and grounded in real WorqAI behavior?",
        ],
    },
    "channel_fit": {
        "intent": "Is it shaped for where it will be published?",
        "questions": [
            "Does the structure match the channel (hook and beats for reels, a slide arc for carousels, and so on)?",
            "Are the length and format right for the destination?",
            "Is the language and market localization correct?",
        ],
    },
}


def build_judge_packet(
    text: str,
    task: MarketingTask,
    brand: BrandMemory,
    gates: tuple[GateResult, ...],
) -> dict[str, object]:
    """Compile everything the operator needs to score the draft as a fresh pass."""

    context = brand.compact_context(task.topic)
    return {
        "instruction": (
            "Score this draft as a separate critical pass, not as the author. Give each axis a "
            "0-5 score, and for every point deducted quote the exact sentence or phrase that "
            "justifies it. Do not reward length: a concise, correct asset can earn full marks. "
            "End with one recommendation: ship or revise, and if revise, name the single weakest axis."
        ),
        "draft": text,
        "task": {
            "asset_type": task.asset_type.value,
            "topic": task.topic,
            "language": task.language,
            "market": task.market,
            "audience": task.audience,
            "objective": task.objective,
            "channel": task.channel,
            "has_source_text": bool(task.source_text.strip()),
        },
        "brand_excerpts": {
            "voice": context["voice"],
            "positioning": context["positioning"],
            "spanish_latam_voice": context["spanish_latam_voice"],
            "banned_language": context["anti_slop"],
        },
        "rubric": JUDGE_RUBRIC,
        "hard_gates": [gate_to_dict(gate) for gate in gates],
    }
