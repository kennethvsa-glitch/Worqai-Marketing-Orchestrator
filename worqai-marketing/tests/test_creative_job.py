from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from scripts import creative_job


def test_approval_is_invalidated_when_slide_changes(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(creative_job, "JOBS", tmp_path / "jobs")
    brief, contract = tmp_path / "brief.md", tmp_path / "art-direction.json"
    html, render, report = tmp_path / "slide.html", tmp_path / "slide.png", tmp_path / "report.json"
    brief.write_text("brief", encoding="utf-8"); contract.write_text("{}", encoding="utf-8")
    html.write_text("<main>approved</main>", encoding="utf-8"); render.write_bytes(b"png"); report.write_text("{}", encoding="utf-8")
    job = creative_job.create(argparse.Namespace(brief=brief))
    creative_job.approve_concept(argparse.Namespace(job_id=job["id"], contract=contract, by="human"))
    creative_job.submit_slide(argparse.Namespace(job_id=job["id"], slide_id="01", html=html, render=render, report=report))
    creative_job.approve_slide(argparse.Namespace(job_id=job["id"], slide_id="01", by="human"))
    assert creative_job.ready(argparse.Namespace(job_id=job["id"]))["ready"] is True
    html.write_text("<main>changed</main>", encoding="utf-8")
    with pytest.raises(ValueError, match="unapproved or changed"):
        creative_job.ready(argparse.Namespace(job_id=job["id"]))
