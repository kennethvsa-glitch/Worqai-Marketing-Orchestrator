"""Dependency-free web search adapter.

The adapter uses DuckDuckGo's HTML endpoint so the project can stay free of API
keys in v1. If a production API is added later, keep this adapter's return
shape and swap the internals.
"""

from __future__ import annotations

from html.parser import HTMLParser
from urllib.error import URLError
from urllib.parse import quote_plus, unquote, urlparse, parse_qs
from urllib.request import Request, urlopen

from ..models import SearchReference


class SearchError(RuntimeError):
    pass


class DuckDuckGoSearchAdapter:
    def search(self, query: str, *, limit: int = 5, timeout: int = 12) -> tuple[SearchReference, ...]:
        urls = (
            f"https://duckduckgo.com/html/?q={quote_plus(query)}",
            f"https://lite.duckduckgo.com/lite/?q={quote_plus(query)}",
        )
        last_error: str | None = None
        for url in urls:
            try:
                results = self._search_url(url, limit=limit, timeout=timeout)
            except SearchError as error:
                last_error = str(error)
                continue
            if results:
                return results
        if last_error:
            raise SearchError(last_error)
        return ()

    def _search_url(self, url: str, *, limit: int, timeout: int) -> tuple[SearchReference, ...]:
        request = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 WorqAI-Marketing-Intelligence/0.1",
            },
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                html = response.read().decode("utf-8", errors="replace")
        except URLError as error:
            raise SearchError(str(error)) from error
        parser = _DuckParser()
        parser.feed(html)
        if not parser.results:
            generic = _GenericLinkParser()
            generic.feed(html)
            return tuple(generic.results[:limit])
        return tuple(parser.results[:limit])


class _DuckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[SearchReference] = []
        self._in_title = False
        self._in_snippet = False
        self._current_url = ""
        self._current_title: list[str] = []
        self._current_snippet: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or "" for key, value in attrs}
        classes = attrs_dict.get("class", "")
        if tag == "a" and "result__a" in classes:
            self._in_title = True
            self._current_url = _clean_duck_url(attrs_dict.get("href", ""))
            self._current_title = []
            self._current_snippet = []
        elif "result__snippet" in classes:
            self._in_snippet = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._in_title:
            self._in_title = False
        if self._in_snippet and tag in {"a", "div"}:
            self._in_snippet = False
            self._commit()

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._current_title.append(data)
        elif self._in_snippet:
            self._current_snippet.append(data)

    def _commit(self) -> None:
        title = " ".join(" ".join(self._current_title).split())
        snippet = " ".join(" ".join(self._current_snippet).split())
        if title and self._current_url:
            self.results.append(
                SearchReference(
                    title=title,
                    url=self._current_url,
                    snippet=snippet,
                    source="duckduckgo",
                )
            )
        self._current_title = []
        self._current_snippet = []
        self._current_url = ""


def _clean_duck_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.path == "/l/":
        uddg = parse_qs(parsed.query).get("uddg", [""])[0]
        return unquote(uddg)
    if "uddg" in parse_qs(parsed.query):
        return unquote(parse_qs(parsed.query).get("uddg", [""])[0])
    return url


class _GenericLinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[SearchReference] = []
        self._in_link = False
        self._href = ""
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attrs_dict = {key: value or "" for key, value in attrs}
        href = _clean_duck_url(attrs_dict.get("href", ""))
        if _is_result_href(href):
            self._in_link = True
            self._href = href
            self._text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._in_link:
            title = " ".join(" ".join(self._text).split())
            if title and self._href:
                self.results.append(
                    SearchReference(
                        title=title,
                        url=self._href,
                        snippet="",
                        source="duckduckgo",
                    )
                )
            self._in_link = False
            self._href = ""
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._in_link:
            self._text.append(data)


def _is_result_href(href: str) -> bool:
    if not href:
        return False
    blocked = (
        "duckduckgo.com",
        "/html/",
        "/lite/",
        "javascript:",
        "#",
    )
    return not any(item in href for item in blocked)
