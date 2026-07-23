"""Request-sensitive campaign strategy assembly."""

from __future__ import annotations

from .copy_engine import clean_topic, cta, hooks, proof_line
from .models import MarketingTask


def build_campaign(task: MarketingTask) -> dict[str, object]:
    topic = clean_topic(task.topic)
    return {
        "campaign_name": _name(task, topic),
        "topic": topic,
        "audience": task.audience,
        "market": task.market,
        "objective": task.objective,
        "core_message": hooks(task)[0],
        "angle_matrix": [
            {"angle": "pain", "idea": f"Show the practical cost when {topic} hides relevant evidence."},
            {"angle": "mechanism", "idea": "Turn vacancy requirements into an explicit evidence map."},
            {"angle": "proof", "idea": proof_line(task)},
            {"angle": "trust", "idea": "Show adaptation using only existing experience and require final human review."},
            {"angle": "action", "idea": cta(task)},
        ],
        "testable_hypotheses": [
            "Before/after evidence will create more saves and qualified clicks than ATS explanation alone.",
            "A real vacancy will create more trust than a generic product walkthrough.",
            "A no-invention boundary will reduce skepticism in comments and replies.",
        ],
        "recommended_assets": [
            "one proof-led reel",
            "one diagnostic carousel",
            "one source-backed community post",
            "one landing or SEO page matching the same intent",
        ],
        "cta": cta(task),
    }


def _name(task: MarketingTask, topic: str) -> str:
    words = [word.capitalize() for word in topic.replace("-", " ").split() if len(word) > 3][:3]
    return " ".join(words) or f"WorqAI {task.market} Campaign"
