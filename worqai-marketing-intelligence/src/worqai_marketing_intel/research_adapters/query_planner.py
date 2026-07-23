"""Build search queries for live benchmark research."""

from __future__ import annotations

from ..models import AssetType, MarketingTask


def build_query(task: MarketingTask) -> str:
    topic = _topic_terms(task.topic)
    if task.asset_type == AssetType.IG_REEL:
        return f"high performing Instagram Reel examples {topic} career job search"
    if task.asset_type == AssetType.CAROUSEL:
        return f"LinkedIn carousel examples {topic}"
    if task.asset_type == AssetType.MOTION_VIDEO:
        return f"best SaaS product launch motion video examples {topic}"
    if task.asset_type == AssetType.LANDING_PAGE:
        return f"high converting SaaS landing page examples {topic}"
    if task.asset_type == AssetType.LINKEDIN_POST:
        return f"viral LinkedIn post examples {topic} career SaaS"
    if task.asset_type == AssetType.AD:
        return f"best SaaS ad examples {topic} career tech"
    if task.asset_type == AssetType.EMAIL:
        return f"successful SaaS launch email examples {topic}"
    if task.asset_type == AssetType.SEO_PAGE:
        return f"{topic} search results resume tool ATS"
    if task.asset_type == AssetType.PARTNERSHIP_PITCH:
        return f"university employability technology pilot partnership examples {topic}"
    if task.asset_type == AssetType.MESSAGE_REPLY:
        return f"career SaaS objection response examples {topic}"
    return f"successful marketing examples {topic} SaaS product launch"


def fallback_queries(task: MarketingTask) -> tuple[str, ...]:
    topic = _topic_terms(task.topic)
    if task.asset_type == AssetType.CAROUSEL:
        return (
            "LinkedIn carousel examples",
            f"career carousel examples {topic}".strip(),
            "resume writing examples LinkedIn",
            "SaaS carousel examples",
        )
    if task.asset_type == AssetType.IG_REEL:
        return (
            f"Instagram Reels resume advice {topic}".strip(),
            "short form career product demo examples",
            "job search Reel before after examples",
        )
    if task.asset_type == AssetType.MOTION_VIDEO:
        return (
            "SaaS product video examples",
            "product launch video examples",
            f"motion video examples {topic}".strip(),
        )
    if task.asset_type == AssetType.LANDING_PAGE:
        return (
            "SaaS landing page examples",
            "high converting landing page examples",
            f"landing page examples {topic}".strip(),
        )
    if task.asset_type == AssetType.SEO_PAGE:
        return (
            f"{topic} CV tool".strip(),
            "cv con ia",
            "analizador cv ats",
            "adaptar cv a vacante",
        )
    if task.asset_type == AssetType.PARTNERSHIP_PITCH:
        return (
            "university career center technology pilot",
            "workforce development software partnership case study",
            f"employability pilot {topic}".strip(),
        )
    return (
        "SaaS marketing examples",
        "product launch examples",
        f"marketing examples {topic}".strip(),
    )


def _topic_terms(topic: str) -> str:
    lowered = topic.lower()
    stopwords = {
        "worqai",
        "create",
        "make",
        "write",
        "for",
        "a",
        "an",
        "the",
        "about",
        "idea",
        "ideas",
        "crea",
        "crear",
        "haz",
        "dame",
        "para",
        "sobre",
        "carrusel",
        "guion",
        "guión",
    }
    words = [word for word in lowered.replace("-", " ").split() if word not in stopwords]
    priority = [word for word in words if word in {"resume", "cv", "career", "job", "ats", "tailoring"}]
    if priority:
        return " ".join(dict.fromkeys(priority))[:80]
    return " ".join(words[:6])[:80]
