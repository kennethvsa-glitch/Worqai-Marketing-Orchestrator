"""Benchmark pattern retrieval and research packaging."""

from __future__ import annotations

from .memory_store import MemoryStore, RankedBenchmarkExample
from .models import AssetType, BenchmarkExample, BenchmarkPattern, MarketingTask
from .pattern_library import PATTERNS
from .research_adapters import LiveResearchRunner


class ResearchEngine:
    """Local benchmark engine.

    Saved examples with performance evidence are selected before source-backed
    examples and the built-in fallback library. The orchestrator contract stays
    unchanged, so learned patterns reach every generation-facing brief.
    """

    def __init__(self, memory_store: MemoryStore | None = None) -> None:
        self.memory_store = memory_store or MemoryStore()

    def patterns_for(
        self,
        task: MarketingTask,
        limit: int = 3,
        *,
        channel: str | None = None,
    ) -> tuple[BenchmarkPattern, ...]:
        if limit <= 0:
            return ()
        selected_channel = channel or _default_channel(task.asset_type)
        ranked = self.memory_store.rank_benchmark_examples(
            asset_type=task.asset_type.value,
            channel=selected_channel,
            limit=limit,
        )
        if not ranked and channel is None:
            ranked = self.memory_store.rank_benchmark_examples(
                asset_type=task.asset_type.value,
                limit=limit,
            )
        learned = [_ranked_pattern(item, task.asset_type) for item in ranked]
        ranked_ids = {item.example.id for item in ranked}
        saved = [
            _saved_pattern(example, task.asset_type)
            for example in self.memory_store.list_benchmark_examples(
                asset_type=task.asset_type.value,
                limit=limit,
            )
            if example.id not in ranked_ids
        ]
        direct = [pattern for pattern in PATTERNS if pattern.asset_type == task.asset_type]
        campaign = [pattern for pattern in PATTERNS if pattern.asset_type == AssetType.CAMPAIGN]
        candidates = learned + saved + direct + campaign
        selected: list[BenchmarkPattern] = []
        seen: set[str] = set()
        for pattern in candidates:
            key = " ".join(pattern.pattern.lower().split())
            if key in seen:
                continue
            seen.add(key)
            selected.append(pattern)
            if len(selected) == limit:
                break
        return tuple(selected)

    def successful_patterns(
        self,
        *,
        asset_type: AssetType | str,
        channel: str | None = None,
        limit: int = 10,
    ) -> tuple[RankedBenchmarkExample, ...]:
        """Expose learned winners for inspection or downstream generation."""

        value = asset_type.value if isinstance(asset_type, AssetType) else str(asset_type)
        return tuple(
            self.memory_store.rank_benchmark_examples(
                asset_type=value,
                channel=channel,
                limit=limit,
            )
        )

    def summarize(self, patterns: tuple[BenchmarkPattern, ...]) -> tuple[str, ...]:
        return tuple(f"{item.name}: {item.pattern}" for item in patterns)

    def live_report(self, task: MarketingTask, *, limit: int = 5):
        return LiveResearchRunner().run(task, limit=limit)

    def url_report(self, task: MarketingTask, url: str):
        return LiveResearchRunner().inspect_url(task, url)


def _ranked_pattern(item: RankedBenchmarkExample, fallback_type: AssetType) -> BenchmarkPattern:
    example = item.example
    metrics = ", ".join(f"{name}={value:g}" for name, value in item.metrics)
    channel = ", ".join(item.channels) or "recorded channels"
    return BenchmarkPattern(
        name=f"Learned winner: {example.title}",
        asset_type=_asset_type(example.asset_type, fallback_type),
        pattern=example.pattern,
        use_when=(
            f"Performance evidence on {channel} ranks this pattern at "
            f"{item.score:.3f} from {item.event_count} event(s): {metrics}."
        ),
        avoid=f"Use the repeatable structure, not wording from {example.source}.",
    )


def _saved_pattern(example: BenchmarkExample, fallback_type: AssetType) -> BenchmarkPattern:
    return BenchmarkPattern(
        name=f"Saved benchmark: {example.title}",
        asset_type=_asset_type(example.asset_type, fallback_type),
        pattern=example.pattern,
        use_when=f"A source-backed example is useful for this asset. Source: {example.source}",
        avoid="Treat this as an unvalidated reference until performance events are recorded.",
    )


def _asset_type(value: str, fallback: AssetType) -> AssetType:
    try:
        return AssetType(value)
    except ValueError:
        return fallback


def _default_channel(asset_type: AssetType) -> str | None:
    if asset_type in {
        AssetType.AD,
        AssetType.CAROUSEL,
        AssetType.IG_REEL,
        AssetType.LINKEDIN_POST,
        AssetType.MOTION_VIDEO,
    }:
        return "social"
    if asset_type in {AssetType.SEO_PAGE, AssetType.LANDING_PAGE}:
        return "seo"
    if asset_type in {AssetType.PARTNERSHIP_PITCH, AssetType.EMAIL, AssetType.MESSAGE_REPLY}:
        return "outreach"
    return None
