"""Serialization helpers for dataclass models."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any


def to_plain(value: Any) -> Any:
    if is_dataclass(value):
        return {key: to_plain(child) for key, child in asdict(value).items()}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {str(key): to_plain(child) for key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_plain(child) for child in value]
    return value
