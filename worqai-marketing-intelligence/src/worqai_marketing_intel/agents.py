"""Agent activation from compact JSON config."""

from __future__ import annotations

import json

from .models import AgentInsight, BenchmarkPattern, MarketingTask
from .paths import config_path


class AgentRegistry:
    def __init__(self) -> None:
        self.data = json.loads(config_path("agents.json").read_text(encoding="utf-8"))

    def active_for(self, task: MarketingTask) -> tuple[str, ...]:
        selected: list[str] = []
        for agent in self.data["agents"]:
            triggers = set(agent["activates_for"])
            if "all" in triggers or task.asset_type.value in triggers:
                selected.append(agent["id"])
        return tuple(selected)

    def insights_for(
        self,
        task: MarketingTask,
        brand_context: dict[str, str],
        patterns: tuple[BenchmarkPattern, ...],
    ) -> tuple[AgentInsight, ...]:
        """Turn configured roles into concrete, generation-facing judgments."""

        active = self.active_for(task)
        pattern_names = tuple(pattern.name for pattern in patterns[:3])
        topic = task.topic
        insights: list[AgentInsight] = []
        for agent_id in active:
            if agent_id == "brand-strategist":
                insights.append(AgentInsight(
                    agent_id=agent_id,
                    focus="positioning",
                    recommendation=(
                        f"Frame {topic} through role-specific evidence and the job description, "
                        "not through generic AI convenience."
                    ),
                    evidence=(brand_context.get("positioning", ""),),
                    risk="Do not drift into resume-template language.",
                ))
            elif agent_id == "market-research-scout":
                insights.append(AgentInsight(
                    agent_id=agent_id,
                    focus="benchmarks",
                    recommendation=(
                        "Use the strongest observed structure, then make the proof and wording "
                        f"specific to {task.audience}."
                    ),
                    evidence=pattern_names,
                    risk="Do not copy source wording or visual identity.",
                ))
            elif agent_id in {"copy-chief", "carousel-architect", "motion-creative-director"}:
                insights.append(AgentInsight(
                    agent_id=agent_id,
                    focus="creative execution",
                    recommendation=(
                        f"Lead with one consequence of {topic}, reveal the mechanism, show proof, "
                        f"and close toward {task.objective}."
                    ),
                    evidence=(f"Channel: {task.channel}", f"Offer: {task.offer}"),
                    risk="Avoid broad claims without a visible example.",
                ))
            elif agent_id in {"growth-strategist", "partnership-pitch-strategist"}:
                insights.append(AgentInsight(
                    agent_id=agent_id,
                    focus="conversion",
                    recommendation=(
                        f"Make the next step proportionate to {task.objective}; use a low-risk "
                        "trial, real vacancy, proof sample, or pilot."
                    ),
                    evidence=(f"Audience: {task.audience}", f"Market: {task.market}"),
                    risk="Do not ask for a large commitment before showing proof.",
                ))
            elif agent_id == "product-marketing-translator":
                insights.append(AgentInsight(
                    agent_id=agent_id,
                    focus="product truth",
                    recommendation="Translate product mechanics into a before/after the audience can inspect.",
                    evidence=("CV + job description -> fit gaps -> truthful adaptation",),
                    risk="Never imply guaranteed ATS passage or interviews.",
                ))
            elif agent_id == "taste-director":
                insights.append(AgentInsight(
                    agent_id=agent_id,
                    focus="taste",
                    recommendation="Prefer one sharp idea, concrete nouns, short sentences, and restrained claims.",
                    evidence=(brand_context.get("voice", ""),),
                    risk="Reject generic SaaS language even when the structure is complete.",
                ))
            elif agent_id == "contrarian-market-critic":
                insights.append(AgentInsight(
                    agent_id=agent_id,
                    focus="challenge",
                    recommendation="Ask what visible evidence would make a skeptical reader believe this claim.",
                    evidence=("Proof must appear before or beside the CTA.",),
                    risk="The asset may explain ATS while failing to demonstrate WorqAI.",
                ))
        return tuple(insights)
