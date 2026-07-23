"""Core models for the marketing intelligence runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class AssetType(StrEnum):
    CAMPAIGN = "campaign"
    CAROUSEL = "carousel"
    IG_REEL = "ig_reel"
    LANDING_PAGE = "landing_page"
    MOTION_VIDEO = "motion_video"
    MOTION_HANDOFF = "motion_handoff"
    LINKEDIN_POST = "linkedin_post"
    PARTNERSHIP_PITCH = "partnership_pitch"
    MESSAGE_REPLY = "message_reply"
    SEO_PAGE = "seo_page"
    CAMPAIGN_PACKAGE = "campaign_package"
    DEEP_RESEARCH = "deep_research"
    FEEDBACK_LOOP = "feedback_loop"
    UNIVERSAL_INTAKE = "universal_intake"
    AD = "ad"
    EMAIL = "email"
    BRAND = "brand"
    RESEARCH = "research"
    CONTENT_SYSTEM = "content_system"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class MarketingTask:
    request: str
    asset_type: AssetType
    topic: str
    audience: str = "job seekers and career operators"
    signals: tuple[str, ...] = ()
    language: str = "en"
    market: str = "LatAm"
    objective: str = "awareness"
    channel: str = ""
    offer: str = "WorqAI"
    source_text: str = ""
    constraints: tuple[str, ...] = ()
    research_requested: bool = False
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class BenchmarkPattern:
    name: str
    asset_type: AssetType
    pattern: str
    use_when: str
    avoid: str
    source: str = "built-in"
    confidence: float = 0.65
    performance_score: float = 0.0


@dataclass(frozen=True)
class AgentInsight:
    agent_id: str
    focus: str
    recommendation: str
    evidence: tuple[str, ...] = ()
    risk: str = ""


@dataclass(frozen=True)
class GenerationPacket:
    task: MarketingTask
    brand_context: dict[str, str]
    benchmark_patterns: tuple[BenchmarkPattern, ...]
    agent_insights: tuple[AgentInsight, ...]
    requirements: tuple[str, ...]
    claims_to_qualify: tuple[str, ...] = ()
    source_facts: tuple[str, ...] = ()


@dataclass(frozen=True)
class WorkspaceRecommendation:
    workspace_id: str
    path: str
    reason: str
    confidence: float


@dataclass(frozen=True)
class QualityScore:
    score: int
    max_score: int
    strengths: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    banned_phrases: tuple[str, ...] = ()


@dataclass(frozen=True)
class MarketingBrief:
    task: MarketingTask
    active_agents: tuple[str, ...]
    strategic_angle: str
    benchmark_patterns: tuple[BenchmarkPattern, ...]
    concept: dict[str, object]
    quality: QualityScore
    workspace: WorkspaceRecommendation
    brand_context: dict[str, str] = field(default_factory=dict)
    agent_insights: tuple[AgentInsight, ...] = field(default_factory=tuple)
    generation_requirements: tuple[str, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    @property
    def audience(self) -> str:
        return self.task.audience

    @property
    def asset_type(self) -> AssetType:
        return self.task.asset_type


@dataclass(frozen=True)
class WorkspaceInspection:
    workspace_id: str
    path: str
    exists: bool
    project_type: str
    is_git_repo: bool
    current_branch: str | None = None
    dirty: bool | None = None
    available_commands: tuple[str, ...] = ()
    asset_destinations: tuple[str, ...] = ()
    important_files: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    access_error: str | None = None


@dataclass(frozen=True)
class WorkspaceActionPlan:
    workspace_id: str
    workspace_path: str
    asset_type: str
    source_request: str
    current_branch: str | None
    dirty: bool | None
    recommended_branch: str
    asset_relative_path: str
    write_mode: str
    can_write: bool
    human_approval_required: bool
    verification_commands: tuple[str, ...] = ()
    safety_notes: tuple[str, ...] = ()
    capability_id: str = "markdown-brief"
    adapter: str = "markdown"
    source_format: str = "markdown"
    output_format: str = "markdown"


@dataclass(frozen=True)
class ActionPlanRecord:
    id: str
    created_at: str
    request: str
    workspace_id: str
    asset_type: str
    status: str


@dataclass(frozen=True)
class BenchmarkExample:
    id: str
    created_at: str
    asset_type: str
    title: str
    source: str
    pattern: str
    notes: str = ""


@dataclass(frozen=True)
class PerformanceEvent:
    id: str
    created_at: str
    asset_id: str
    asset_type: str
    channel: str
    metric_name: str
    metric_value: float
    notes: str = ""


@dataclass(frozen=True)
class ProductionResult:
    plan_id: str
    workspace_id: str
    destination_path: str
    dry_run: bool
    wrote: bool
    verification_commands: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class SearchReference:
    title: str
    url: str
    snippet: str
    source: str
    content_excerpt: str = ""


@dataclass(frozen=True)
class ExtractedResearchPattern:
    asset_type: str
    title: str
    source: str
    pattern: str
    notes: str
    confidence: float


@dataclass(frozen=True)
class LiveResearchReport:
    asset_type: str
    query: str
    references: tuple[SearchReference, ...] = ()
    extracted_patterns: tuple[ExtractedResearchPattern, ...] = ()
    warnings: tuple[str, ...] = ()
