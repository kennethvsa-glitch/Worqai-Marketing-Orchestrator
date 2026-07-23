"""Live benchmark research orchestration."""

from __future__ import annotations

from collections.abc import Callable

from ..models import LiveResearchReport, MarketingTask, SearchReference
from .pattern_extractor import extract_patterns
from .page_fetcher import PageFetchError, fetch_reference
from .query_planner import build_query, fallback_queries
from .web_search import DuckDuckGoSearchAdapter, SearchError


class LiveResearchRunner:
    def __init__(
        self,
        search_adapter: DuckDuckGoSearchAdapter | None = None,
        *,
        page_fetcher: Callable[[str], SearchReference] | None = fetch_reference,
    ) -> None:
        self.search_adapter = search_adapter or DuckDuckGoSearchAdapter()
        self.page_fetcher = page_fetcher

    def run(self, task: MarketingTask, *, limit: int = 5) -> LiveResearchReport:
        queries = (build_query(task), *fallback_queries(task))
        warnings: list[str] = []
        references = ()
        selected_query = queries[0]
        try:
            for query in queries:
                selected_query = query
                references = self.search_adapter.search(query, limit=limit)
                if references:
                    break
        except SearchError as error:
            return LiveResearchReport(
                asset_type=task.asset_type.value,
                query=selected_query,
                warnings=(f"Live search failed: {error}",),
            )
        if not references:
            warnings.append("Live search returned no references after fallback queries.")
        references, fetch_warnings = self._enrich_references(references)
        warnings.extend(fetch_warnings)
        patterns = extract_patterns(task, references)
        return LiveResearchReport(
            asset_type=task.asset_type.value,
            query=selected_query,
            references=references,
            extracted_patterns=patterns,
            warnings=tuple(warnings),
        )

    def inspect_url(self, task: MarketingTask, url: str) -> LiveResearchReport:
        try:
            reference = fetch_reference(url)
        except PageFetchError as error:
            return LiveResearchReport(
                asset_type=task.asset_type.value,
                query=url,
                warnings=(f"URL fetch failed: {error}",),
            )
        references = (reference,)
        return LiveResearchReport(
            asset_type=task.asset_type.value,
            query=url,
            references=references,
            extracted_patterns=extract_patterns(task, references),
        )

    def _enrich_references(
        self,
        references: tuple[SearchReference, ...],
    ) -> tuple[tuple[SearchReference, ...], tuple[str, ...]]:
        if self.page_fetcher is None:
            return references, ()
        enriched: list[SearchReference] = []
        warnings: list[str] = []
        for reference in references:
            try:
                fetched = self.page_fetcher(reference.url)
            except (PageFetchError, TimeoutError, OSError) as error:
                enriched.append(reference)
                warnings.append(f"Page fetch failed for {reference.url}: {error}")
                continue
            page_text = fetched.snippet.strip()
            if not page_text:
                enriched.append(reference)
                warnings.append(f"Page fetch returned no readable text for {reference.url}.")
                continue
            enriched.append(
                SearchReference(
                    title=fetched.title if fetched.title != reference.url else reference.title,
                    url=reference.url,
                    snippet=page_text,
                    source=f"{reference.source}+page",
                )
            )
        return tuple(enriched), tuple(warnings)
