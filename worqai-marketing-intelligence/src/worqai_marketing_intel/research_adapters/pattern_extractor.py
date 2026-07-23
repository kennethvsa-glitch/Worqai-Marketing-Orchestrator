"""Heuristic pattern extraction from live references."""

from __future__ import annotations

from ..models import ExtractedResearchPattern, MarketingTask, SearchReference


def extract_patterns(
    task: MarketingTask,
    references: tuple[SearchReference, ...],
) -> tuple[ExtractedResearchPattern, ...]:
    extracted: list[ExtractedResearchPattern] = []
    for reference in references:
        pattern = _infer_pattern(reference.title, reference.snippet)
        if not pattern:
            continue
        extracted.append(
            ExtractedResearchPattern(
                asset_type=task.asset_type.value,
                title=reference.title,
                source=reference.url,
                pattern=pattern,
                notes=_notes(reference),
                confidence=_confidence(reference),
            )
        )
    return tuple(extracted)


def _infer_pattern(title: str, snippet: str) -> str:
    text = f"{title} {snippet}".lower()
    if any(word in text for word in ("teardown", "mistake", "fails", "failure")):
        return "Use a teardown structure: identify the common mistake, explain why it fails, then show the better operating rule."
    if any(word in text for word in ("before", "after", "case study")):
        return "Use a proof-led before/after structure: show the starting state, the mechanism, and the improved result."
    if any(word in text for word in ("template", "checklist", "framework")):
        return "Use a practical framework: make the asset feel immediately usable, not motivational."
    if any(word in text for word in ("launch", "product", "demo")):
        return "Use product evidence as the story: show the workflow or artifact instead of abstract claims."
    if any(word in text for word in ("linkedin", "carousel", "post")):
        return "Use a social-native hook: specific tension first, compact teaching second, practical CTA last."
    return "Extract the asset's repeatable structure, then translate it into a WorqAI-native concept without copying words or visuals."


def _notes(reference: SearchReference) -> str:
    snippet = reference.snippet.strip()
    if not snippet:
        return "Search result provided no snippet; inspect source before production use."
    evidence_type = "fetched page text" if "+page" in reference.source else "search snippet"
    return f"Observed from {evidence_type}: {snippet[:500]}"


def _confidence(reference: SearchReference) -> float:
    score = 0.45
    if reference.snippet:
        score += 0.2
    if "+page" in reference.source:
        score += 0.1
    lowered = f"{reference.title} {reference.snippet}".lower()
    if any(word in lowered for word in ("example", "case study", "teardown", "template", "framework")):
        score += 0.2
    return min(score, 0.9)
