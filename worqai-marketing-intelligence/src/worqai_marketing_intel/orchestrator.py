"""Marketing orchestration runtime."""

from __future__ import annotations

from .agents import AgentRegistry
from .action_planner import ActionPlanner
from .artifact_writer import ArtifactWriter
from .brand_memory import BrandMemory
from .campaign_engine import build_campaign
from .campaign_package_engine import build_campaign_package
from .codec import to_plain
from .carousel_engine import build_carousel
from .copy_engine import strategic_angle
from .deep_research_engine import build_deep_research_plan
from .execution_engine import ExecutionEngine
from .feedback_engine import build_feedback_loop
from .models import AssetType, MarketingBrief
from .generation_contract import build_generation_packet
from .motion_handoff_engine import build_motion_handoff
from .motion_brief_engine import build_motion_brief
from .pitch_engine import build_partnership_pitch
from .research_engine import ResearchEngine
from .reel_script_engine import build_reel_script
from .router import classify
from .script_audit_engine import audit_script
from .seo_engine import build_seo_plan
from .message_reply_engine import build_message_reply
from .taste_judge import TasteJudge
from .workspace_manager import WorkspaceManager
from .workspace_inspector import WorkspaceInspector
from .workspace_writer import WorkspaceWriter


class MarketingOrchestrator:
    def __init__(self) -> None:
        self.brand = BrandMemory()
        self.research = ResearchEngine()
        self.taste = TasteJudge(self.brand)
        self.workspaces = WorkspaceManager()
        self.workspace_inspector = WorkspaceInspector()
        self.action_planner = ActionPlanner()
        self.workspace_writer = WorkspaceWriter()
        self.execution_engine = ExecutionEngine()
        self.agents = AgentRegistry()

    def brief(self, request: str) -> MarketingBrief:
        task = classify(request)
        patterns = self.research.patterns_for(task)
        brand_context = self.brand.compact_context(task.topic)
        agent_insights = self.agents.insights_for(task, brand_context, patterns)
        packet = build_generation_packet(task, brand_context, patterns, agent_insights)
        active_agents = tuple(insight.agent_id for insight in agent_insights)
        concept = self._build_concept(task)
        # Judge the generated asset itself, not the safety constraints attached below.
        text_for_scoring = _concept_text(concept)
        quality = self.taste.score_asset(text_for_scoring, asset_type=task.asset_type, task=task)
        concept["intelligence"] = {
            "benchmark_patterns": [pattern.name for pattern in patterns],
            "agent_recommendations": [insight.recommendation for insight in agent_insights],
            "generation_requirements": list(packet.requirements),
            "claims_to_qualify": list(packet.claims_to_qualify),
            "source_facts": list(packet.source_facts),
        }
        workspace = self.workspaces.recommend(task)
        return MarketingBrief(
            task=task,
            active_agents=active_agents,
            strategic_angle=strategic_angle(task),
            benchmark_patterns=patterns,
            concept=concept,
            quality=quality,
            workspace=workspace,
            brand_context=brand_context,
            agent_insights=agent_insights,
            generation_requirements=packet.requirements,
            notes=(
                "Generation uses structured request context, brand rules, saved research, and performance-ranked patterns.",
                "For source-backed current research, run live research before final factual claims.",
                "Claude supplies novel creative reasoning; Python compiles context, validates, learns, and routes production.",
            ),
        )

    def prepare(self, request: str):
        """Return the compact intelligence packet used by Claude generation."""

        task = classify(request)
        patterns = self.research.patterns_for(task)
        brand_context = self.brand.compact_context(task.topic)
        insights = self.agents.insights_for(task, brand_context, patterns)
        return build_generation_packet(task, brand_context, patterns, insights)

    def route(self, request: str):
        return self.workspaces.recommend(classify(request))

    def score(self, text: str):
        return self.taste.score(text)

    def audit_script(self, request: str, script: str):
        task = classify(request)
        return audit_script(task, script)

    def message_reply(self, request: str, message: str):
        return build_message_reply(request, message)

    def brief_dict(self, request: str) -> dict[str, object]:
        return to_plain(self.brief(request))

    def write_brief(self, brief: MarketingBrief, *, record_id: str | None = None):
        return ArtifactWriter().write_brief(brief, record_id=record_id)

    def inspect_workspaces(self):
        return self.workspace_inspector.inspect_all()

    def live_research(self, request: str, *, limit: int = 5):
        task = classify(request)
        return self.research.live_report(task, limit=limit)

    def research_url(self, request: str, url: str):
        task = classify(request)
        return self.research.url_report(task, url)

    def action_plan(self, request: str):
        brief = self.brief(request)
        inspections = self.inspect_workspaces()
        return brief, self.action_planner.plan(brief, inspections)

    def produce_from_payload(
        self,
        *,
        plan_id: str,
        plan_payload: dict[str, object],
        brief_payload: dict[str, object],
        dry_run: bool = True,
    ):
        from .workspace_writer import plan_from_payload

        plan = plan_from_payload(plan_payload)
        return self.workspace_writer.write_payload(
            plan_id=plan_id,
            plan=plan,
            brief_payload=brief_payload,
            dry_run=dry_run,
        )

    def execute_from_payload(
        self,
        *,
        plan_id: str,
        plan_payload: dict[str, object],
        brief_payload: dict[str, object],
        dry_run: bool = True,
        create_branch: bool = False,
        verify: bool = False,
        allow_dirty: bool = False,
    ):
        return self.execution_engine.execute(
            plan_id=plan_id,
            plan_payload=plan_payload,
            brief_payload=brief_payload,
            dry_run=dry_run,
            create_branch=create_branch,
            verify=verify,
            allow_dirty=allow_dirty,
        )

    def _build_concept(self, task):
        if task.asset_type == AssetType.IG_REEL:
            return build_reel_script(task)
        if task.asset_type == AssetType.CAROUSEL:
            return build_carousel(task)
        if task.asset_type == AssetType.MOTION_VIDEO:
            return build_motion_brief(task)
        if task.asset_type == AssetType.MOTION_HANDOFF:
            return build_motion_handoff(task)
        if task.asset_type == AssetType.PARTNERSHIP_PITCH:
            return build_partnership_pitch(task)
        if task.asset_type == AssetType.SEO_PAGE:
            return build_seo_plan(task)
        if task.asset_type == AssetType.CAMPAIGN_PACKAGE:
            return build_campaign_package(task)
        if task.asset_type == AssetType.DEEP_RESEARCH:
            return build_deep_research_plan(task.request)
        if task.asset_type == AssetType.FEEDBACK_LOOP:
            return build_feedback_loop(task.request)
        if task.asset_type == AssetType.MESSAGE_REPLY:
            return build_message_reply(task.request, task.source_text or task.request)
        return build_campaign(task)


def _concept_text(concept: dict[str, object]) -> str:
    parts: list[str] = []
    for value in concept.values():
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            parts.extend(str(item) for item in value)
        else:
            parts.append(str(value))
    return "\n".join(parts)
