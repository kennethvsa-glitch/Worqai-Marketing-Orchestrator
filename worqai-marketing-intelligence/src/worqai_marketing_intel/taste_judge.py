"""Advisory quality scoring for marketing outputs.

This is a heuristic *advisory* signal, not a gate. The deterministic pass/fail
gates live in ``validation``; substantive quality judgment is performed by the
creative operator against the judge packet. The numeric score here is retained
for backward compatibility (briefs, history) and as a rough smoke signal.
"""

from __future__ import annotations

from .brand_memory import BrandMemory
from .models import AssetType, MarketingTask, QualityScore
from .quality_rubric import asset_rubric
from .text_signals import (
    has_clear_cta_or_next_step,
    has_specificity,
    looks_spanish,
    matches_topic,
    preserves_source,
    risky_claims,
)


class TasteJudge:
    def __init__(self, brand: BrandMemory) -> None:
        self.brand = brand

    def score(self, text: str) -> QualityScore:
        return self.score_asset(text, asset_type=None)

    def score_asset(
        self,
        text: str,
        asset_type: AssetType | None = None,
        task: MarketingTask | None = None,
    ) -> QualityScore:
        lowered = text.lower()
        banned = tuple(phrase for phrase in self.brand.banned_phrases() if phrase in lowered)
        score = 10
        risks: list[str] = []
        strengths: list[str] = []

        if banned:
            score -= min(4, len(banned) * 2)
            risks.append("Contains banned generic marketing language.")
        else:
            strengths.append("Avoids the known anti-slop phrase list.")

        if has_specificity(text):
            strengths.append("Includes concrete product or audience detail.")
        else:
            score -= 2
            risks.append("Needs more concrete product or audience detail.")

        if has_clear_cta_or_next_step(text):
            strengths.append("Has a practical next step or CTA.")
        else:
            score -= 1
            risks.append("CTA or next step could be sharper.")

        if len(text.split()) < 60:
            score -= 1
            risks.append("Output may be too thin for professional use.")

        if task is not None:
            if matches_topic(text, task.topic):
                strengths.append("The output is specific to the requested topic.")
            else:
                score -= 2
                risks.append("The output does not visibly use the requested topic.")

            if task.source_text:
                if preserves_source(text, task.source_text):
                    strengths.append("Preserves meaningful source material.")
                else:
                    score -= 2
                    risks.append("Rewrite may have replaced rather than preserved the source idea.")

            if task.language.lower().startswith("es"):
                if looks_spanish(text):
                    strengths.append("Uses Spanish/LatAm language signals.")
                else:
                    score -= 1
                    risks.append("Requested Spanish output is not clearly localized.")

        risky = risky_claims(text)
        if risky:
            score -= min(2, len(risky))
            risks.append("Contains absolute claims that need qualification: " + ", ".join(risky))
        else:
            strengths.append("Avoids known absolute outcome and ATS claims.")

        if asset_type is not None:
            penalty, rubric_strengths, rubric_risks = asset_rubric(asset_type, text)
            score -= penalty
            strengths.extend(rubric_strengths)
            risks.extend(rubric_risks)

        return QualityScore(
            score=max(score, 0),
            max_score=10,
            strengths=tuple(strengths),
            risks=tuple(risks),
            banned_phrases=banned,
        )
