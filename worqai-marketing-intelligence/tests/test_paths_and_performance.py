from worqai_marketing_intel import paths
from worqai_marketing_intel.cli import _parse_performance
from worqai_marketing_intel.memory_store import MemoryStore


def test_data_home_respects_wmi_home(monkeypatch, tmp_path):
    monkeypatch.setenv("WMI_HOME", str(tmp_path / "home"))
    assert paths.data_home() == tmp_path / "home"
    assert paths.memory_db_path() == tmp_path / "home" / "memory.db"


def test_memory_store_default_honors_wmi_home_without_migration(monkeypatch, tmp_path):
    monkeypatch.setenv("WMI_HOME", str(tmp_path / "home"))
    monkeypatch.setattr(paths, "legacy_memory_db_path", lambda: tmp_path / "absent" / "memory.db")

    store = MemoryStore()
    assert store.path == tmp_path / "home" / "memory.db"
    assert store.path.exists()


def test_legacy_db_is_migrated_once(monkeypatch, tmp_path):
    legacy = tmp_path / "repo" / ".wmi" / "memory.db"
    legacy.parent.mkdir(parents=True)
    MemoryStore(legacy).save_performance_text(
        asset_id="a1", asset_type="reel", channel="ig", text="10 saves"
    )

    target = tmp_path / "home" / "memory.db"
    monkeypatch.setenv("WMI_HOME", str(tmp_path / "home"))
    monkeypatch.setattr(paths, "legacy_memory_db_path", lambda: legacy)

    store = MemoryStore()
    assert store.path == target
    assert store.list_performance_events(asset_type="reel"), "migrated rows should be present"


def test_sqlite_backup_roundtrip(tmp_path):
    src = tmp_path / "src.db"
    dst = tmp_path / "dst.db"
    MemoryStore(src).save_performance_text(
        asset_id="a1", asset_type="reel", channel="ig", text="10 saves"
    )

    paths._sqlite_backup(src, dst)
    assert MemoryStore(dst).list_performance_events(asset_type="reel")


def test_record_performance_canonicalizes_bilingual_metrics(tmp_path):
    store = MemoryStore(tmp_path / "memory.db")
    store.save_performance_text(
        asset_id="a1",
        asset_type="carousel",
        channel="linkedin",
        text="42 guardados y 8 registros",
    )
    metrics = {event.metric_name for event in store.list_performance_events(asset_type="carousel")}
    assert "saves" in metrics
    assert "signups" in metrics


def test_parse_performance_requires_four_fields():
    import pytest

    with pytest.raises(SystemExit):
        _parse_performance("a1 | carousel | linkedin")

    parsed = _parse_performance("a1 | carousel | linkedin | 42 saves and 8 signups")
    assert parsed == {
        "asset_id": "a1",
        "asset_type": "carousel",
        "channel": "linkedin",
        "text": "42 saves and 8 signups",
    }
