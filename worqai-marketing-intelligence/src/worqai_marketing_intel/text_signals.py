"""Shared, deterministic text detectors.

These are the single source of truth for cheap heuristic checks used by both
``taste_judge`` (advisory scoring) and ``validation`` (hard gates). Keeping them
here avoids two divergent copies of the same regexes. Behavior must stay stable:
the taste judge's tests assert on scores derived from these functions.
"""

from __future__ import annotations

import re

_TOPIC_STOPWORDS = {
    "a", "about", "and", "create", "for", "idea", "ideas", "make", "of", "para",
    "sobre", "the", "un", "una", "worqai", "write",
}

_SPECIFICITY_SIGNALS = (
    "resume", "job description", "ats", "interview", "role-specific", "application",
)

_CTA_SIGNALS = ("cta", "next step", "try", "use", "send", "book", "start", "compare")

_SPANISH_SIGNALS = (
    "vacante", "experiencia", "puesto", "usted", "reclut", "evidencia", "puede", "para",
)

_RISKY_CLAIM_PATTERNS = (
    "guaranteed interviews", "guaranteed job", "always passes", "all ats",
    "entrevistas garantizadas", "trabajo garantizado", "todos los ats",
    "un humano nunca", "siempre pasa",
)


def has_specificity(text: str) -> bool:
    lowered = text.lower()
    return any(signal in lowered for signal in _SPECIFICITY_SIGNALS) or bool(re.search(r"\d+", text))


def has_clear_cta_or_next_step(text: str) -> bool:
    lowered = text.lower()
    return any(signal in lowered for signal in _CTA_SIGNALS)


def matches_topic(text: str, topic: str) -> bool:
    tokens = {
        token
        for token in re.findall(r"[a-záéíóúñ0-9]+", topic.lower())
        if len(token) > 3 and token not in _TOPIC_STOPWORDS
    }
    if not tokens:
        return True
    lowered = text.lower()
    return any(token in lowered for token in tokens)


def preserves_source(text: str, source: str) -> bool:
    source_tokens = {
        token
        for token in re.findall(r"[a-záéíóúñ0-9]+", source.lower())
        if len(token) > 5
    }
    if not source_tokens:
        return True
    output_tokens = set(re.findall(r"[a-záéíóúñ0-9]+", text.lower()))
    overlap = len(source_tokens & output_tokens) / len(source_tokens)
    return overlap >= 0.2


def looks_spanish(text: str) -> bool:
    lowered = text.lower()
    return bool(re.search(r"[áéíóúñ¿¡]", lowered)) or sum(
        signal in lowered for signal in _SPANISH_SIGNALS
    ) >= 2


def risky_claims(text: str) -> tuple[str, ...]:
    lowered = text.lower()
    return tuple(pattern for pattern in _RISKY_CLAIM_PATTERNS if pattern in lowered)
