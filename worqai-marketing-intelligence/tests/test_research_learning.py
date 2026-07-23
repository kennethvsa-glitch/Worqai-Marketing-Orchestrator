from worqai_marketing_intel.deep_research_engine import build_deep_research_plan
from worqai_marketing_intel.feedback_engine import parse_metric_value, parse_metrics
from worqai_marketing_intel.memory_store import MemoryStore
from worqai_marketing_intel.models import AssetType, MarketingTask, SearchReference
from worqai_marketing_intel.research_adapters.live_research import LiveResearchRunner
from worqai_marketing_intel.research_adapters.page_fetcher import PageFetchError
from worqai_marketing_intel.research_engine import ResearchEngine


def _task(asset_type: AssetType = AssetType.CAROUSEL) -> MarketingTask:
    return MarketingTask(
        request="Create a WorqAI carousel about ATS resumes",
        asset_type=asset_type,
        topic="ATS resume tailoring",
    )


def test_natural_language_metrics_parse_compact_values_and_decimal_commas():
    parsed = parse_metrics(
        "The post got 1,250 impressions, CTR: 3,5%, 42 saves and 2.4k views."
    )

    assert [(metric.name, metric.value) for metric in parsed] == [
        ("impressions", 1250.0),
        ("ctr", 3.5),
        ("saves", 42.0),
        ("views", 2400.0),
    ]
    assert parse_metric_value("1,2 mil") == 1200.0


def test_performance_ranking_prefers_outcomes_and_reaches_generation(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")
    winner_id = store.save_benchmark_example(
        asset_type="carousel",
        title="Proof carousel",
        source="https://example.com/proof",
        pattern="Show a role-specific before and after with visible evidence.",
    )
    reach_id = store.save_benchmark_example(
        asset_type="carousel",
        title="Reach carousel",
        source="https://example.com/reach",
        pattern="Lead with a broad category observation.",
    )
    parsed_ids = store.save_performance_text(
        asset_id=winner_id,
        asset_type="carousel",
        channel="social",
        text="8 signups",
    )
    store.save_performance_event(
        asset_id=reach_id,
        asset_type="carousel",
        channel="social",
        metric_name="impressions",
        metric_value=20000,
    )

    ranked = store.rank_benchmark_examples(asset_type="carousel", channel="social")
    selected = ResearchEngine(store).patterns_for(_task(), channel="social")

    assert len(parsed_ids) == 1
    assert [item.example.id for item in ranked] == [winner_id, reach_id]
    assert ranked == store.rank_benchmark_examples(asset_type="carousel", channel="social")
    assert ranked[0].score > ranked[1].score
    assert selected[0].pattern == "Show a role-specific before and after with visible evidence."
    assert selected[0].name.startswith("Learned winner")


def test_lower_average_position_ranks_better_deterministically(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")
    first = store.save_benchmark_example(
        asset_type="seo_page",
        title="Intent page",
        source="https://example.com/intent",
        pattern="Build around one exact search intent.",
    )
    second = store.save_benchmark_example(
        asset_type="seo_page",
        title="Broad page",
        source="https://example.com/broad",
        pattern="Cover several related search intents.",
    )
    for asset_id, position in ((first, 3.0), (second, 12.0)):
        store.save_performance_event(
            asset_id=asset_id,
            asset_type="seo_page",
            channel="seo",
            metric_name="average position",
            metric_value=position,
        )

    ranked = store.rank_benchmark_examples(asset_type="seo_page", channel="seo")

    assert [item.example.id for item in ranked] == [first, second]
    assert ranked[0].metrics == (("average_position", 3.0),)


def test_live_research_uses_fetched_page_text_for_extraction():
    class FakeSearch:
        def search(self, query, *, limit=5):
            return (
                SearchReference(
                    title="Generic result",
                    url="https://example.com/case-study",
                    snippet="A result without structural clues.",
                    source="fake",
                ),
            )

    def fake_fetch(url):
        return SearchReference(
            title="Resume case study",
            url=url,
            snippet="This case study shows the before state, the mechanism, and the after result.",
            source="url",
        )

    report = LiveResearchRunner(FakeSearch(), page_fetcher=fake_fetch).run(_task())

    assert report.references[0].source == "fake+page"
    assert "before/after" in report.extracted_patterns[0].pattern.lower()
    assert "fetched page text" in report.extracted_patterns[0].notes


def test_live_research_retains_search_evidence_when_page_fetch_is_offline():
    class FakeSearch:
        def search(self, query, *, limit=5):
            return (
                SearchReference(
                    title="Carousel teardown",
                    url="https://offline.example/teardown",
                    snippet="A teardown of a common resume mistake.",
                    source="fake",
                ),
            )

    def offline_fetch(url):
        raise PageFetchError("offline")

    report = LiveResearchRunner(FakeSearch(), page_fetcher=offline_fetch).run(_task())

    assert report.references[0].source == "fake"
    assert report.extracted_patterns
    assert report.warnings == (
        "Page fetch failed for https://offline.example/teardown: offline",
    )


def test_deep_research_report_links_findings_to_supplied_sources():
    source = SearchReference(
        title="ATS resume case study",
        url="https://example.com/ats-case-study",
        snippet="A before and after case study with a role-specific resume rewrite.",
        source="provided",
    )

    report = build_deep_research_plan("Research ATS resume competitors", sources=(source,))

    assert report["format"] == "deep research report"
    assert report["status"] == "evidence_collected"
    assert report["source_register"][0]["id"] == "S1"
    assert report["findings"][0]["source_ids"] == ["S1"]
    assert report["execution_queue"][0]["adapter"] == "DuckDuckGoSearchAdapter.search"
    assert report["completion_criteria"]


def test_deep_research_without_sources_blocks_premature_decisions():
    report = build_deep_research_plan("Research ATS resume competitors")

    assert report["status"] == "research_pending"
    assert report["findings"] == []
    assert report["decisions"][0]["status"] == "pending"
    assert report["execution_queue"]
