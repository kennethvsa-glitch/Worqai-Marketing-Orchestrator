"""Path helpers for package-local source files and runtime state.

Source files (config, brand) live inside the repository. Mutable runtime
state (the SQLite memory database) lives *outside* the repository under a
per-user data home, so a synced folder such as OneDrive can never grab a live
SQLite file mid-write and corrupt it. See ``default_memory_path`` for the
one-time migration from the historical in-repo ``.wmi/memory.db`` location.
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def config_path(name: str) -> Path:
    return project_root() / "config" / name


def brand_path(name: str) -> Path:
    return project_root() / "brand" / name


def data_home() -> Path:
    """Return the writable home for WMI runtime state.

    Precedence:
      1. ``$WMI_HOME`` — explicit override (used by tests and power users).
      2. ``%LOCALAPPDATA%\\wmi`` on Windows.
      3. ``$XDG_DATA_HOME/wmi`` or ``~/.local/share/wmi`` elsewhere.
    """

    override = os.environ.get("WMI_HOME")
    if override:
        return Path(override).expanduser()
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            return Path(local_app_data) / "wmi"
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        return Path(xdg_data_home) / "wmi"
    return Path.home() / ".local" / "share" / "wmi"


def memory_db_path() -> Path:
    """Target location for the SQLite memory database (outside the repo)."""

    return data_home() / "memory.db"


def legacy_memory_db_path() -> Path:
    """Historical in-repo location, kept only for one-time migration."""

    return project_root() / ".wmi" / "memory.db"


def default_memory_path() -> Path:
    """Resolve the memory database path, migrating legacy data once.

    A fresh install uses the out-of-repo location directly. An existing install
    with an in-repo ``.wmi/memory.db`` is migrated once using SQLite's backup
    API (a consistent copy that folds in committed WAL content). If migration
    fails for any reason, the legacy path is used in place so no data is lost.
    """

    target = memory_db_path()
    if target.exists():
        return target
    legacy = legacy_memory_db_path()
    if not legacy.exists():
        return target

    staging = target.with_name(target.name + ".migrating")
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        staging.unlink(missing_ok=True)
        _sqlite_backup(legacy, staging)
        staging.replace(target)
        return target
    except Exception as exc:  # pragma: no cover - defensive fallback
        staging.unlink(missing_ok=True)
        print(
            f"[wmi] memory.db migration to {target} failed ({exc}); "
            f"continuing with legacy path {legacy}",
            file=sys.stderr,
        )
        return legacy


def _sqlite_backup(source: Path, destination: Path) -> None:
    src = sqlite3.connect(source)
    try:
        dst = sqlite3.connect(destination)
        try:
            src.backup(dst)
        finally:
            dst.close()
    finally:
        src.close()
