"""Load compact brand memory from markdown source files."""

from __future__ import annotations

import re

from .paths import brand_path


class BrandMemory:
    """Markdown-backed source of truth with compact runtime accessors."""

    def __init__(self) -> None:
        self.voice = _read("voice.md")
        self.positioning = _read("positioning.md")
        self.anti_slop = _read("anti-slop.md")
        self.anti_generic_creative = _read("anti-generic-creative.md")
        self.benchmark_principles = _read("benchmark-principles.md")
        self.spanish_latam_voice = _read("spanish-latam-voice.md")

    def banned_phrases(self) -> tuple[str, ...]:
        phrases: list[str] = []
        capture = False
        for line in self.anti_slop.splitlines():
            if line.lower().startswith("ban or heavily penalize"):
                capture = True
                continue
            if capture and line.startswith("#"):
                break
            if capture and line.strip().startswith("-"):
                phrases.append(line.strip()[1:].strip().lower())
        return tuple(phrases)

    def compact_context(self, topic: str) -> dict[str, str]:
        return {
            "voice": _first_sentences(self.voice, 8),
            "positioning": _first_sentences(self.positioning, 8),
            "spanish_latam_voice": _first_sentences(self.spanish_latam_voice, 8),
            "anti_slop": ", ".join(self.banned_phrases()),
            "anti_generic_creative": _first_sentences(self.anti_generic_creative, 12),
            "topic": topic,
        }


def _read(name: str) -> str:
    return brand_path(name).read_text(encoding="utf-8")


def _first_sentences(text: str, limit: int) -> str:
    normalized = re.sub(r"\s+", " ", text.replace("#", " ")).strip()
    parts = re.split(r"(?<=[.!?])\s+", normalized)
    return " ".join(parts[:limit])
