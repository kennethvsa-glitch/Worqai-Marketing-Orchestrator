"""Small URL fetcher for direct reference inspection."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ..models import SearchReference


class PageFetchError(RuntimeError):
    pass


def fetch_page_text(url: str, *, timeout: int = 12, max_chars: int = 12000) -> str:
    request = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 WorqAI-Marketing-Intelligence/0.1"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("content-type", "")
            raw = response.read(max_chars * 4)
    except (HTTPError, URLError, TimeoutError, ValueError, OSError) as error:
        raise PageFetchError(str(error)) from error
    if "text" not in content_type and "html" not in content_type:
        return ""
    html = raw.decode("utf-8", errors="replace")
    parser = _TextParser()
    parser.feed(html)
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip()[:max_chars]


def fetch_reference(
    url: str,
    *,
    timeout: int = 12,
    max_chars: int = 12000,
) -> SearchReference:
    request = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 WorqAI-Marketing-Intelligence/0.1"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("content-type", "")
            raw = response.read(max_chars * 4)
    except (HTTPError, URLError, TimeoutError, ValueError, OSError) as error:
        raise PageFetchError(str(error)) from error
    if "text" not in content_type and "html" not in content_type:
        raise PageFetchError(f"Unsupported content type: {content_type}")
    html = raw.decode("utf-8", errors="replace")
    parser = _TextParser()
    parser.feed(html)
    title = parser.title or url
    snippet = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()[:max_chars]
    return SearchReference(title=title, url=url, snippet=snippet, source="url")


class _TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._skip = False
        self._in_title = False
        self._title: list[str] = []

    @property
    def title(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self._title)).strip()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip = True
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip = False
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title.append(data)
        if not self._skip:
            text = data.strip()
            if text:
                self.parts.append(text)
