#!/usr/bin/env python3
"""
Quantum V4 Manual Bypass — Phase 1: Plan Injection + Worktree Creation

Run this when the Claude CLI provider hits a session limit during planning.
It manually creates the plan, transitions states, and sets up the worktree.

Usage:
    python quantum_bypass_phase1.py <RUN_ID>

Prerequisites:
- The run must already exist in the database (created via `q new`)
- The run must be at `spec_approval` or `planning` state
- You need the base SHA (current HEAD of the repo)
"""

import sys
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone

# Add Quantum V4 to path
sys.path.insert(0, "C:/Users/kenne/OneDrive/Documentos/manifest-claude-system/quantum-v4/src")

from quantum_v4.database import Database
from quantum_v4.repository import Repository
from quantum_v4.models import (
    Run, SpecVersion, PlanVersion, Task, TaskStatus,
    Approval, ApprovalStatus, RunStatus
)
from quantum_v4.state_machine import StateMachine
from quantum_v4.worktrees import GitWorktreeManager


def _git_bytes(path, *args):
    completed = subprocess.run(
        ["git", "-C", str(path), *args], capture_output=True, check=False
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.decode(errors="replace").strip())
    return completed.stdout


def _git(path, *args):
    return _git_bytes(path, *args).decode("utf-8").strip()


def _candidate_hash(worktree_path, base_sha):
    """Compute SHA-256 of worktree diff against base SHA."""
    digest = hashlib.sha256()
    digest.update(_git_bytes(worktree_path, "diff", "--binary", base_sha))
    for relative in _git(worktree_path, "ls-files", "--others", "--exclude-standard").splitlines():
        digest.update(relative.encode("utf-8"))
        digest.update(b"\x00")
        digest.update((worktree_path / relative).read_bytes())
    return digest.hexdigest()


def main():
    if len(sys.argv) < 2:
        print("Usage: python quantum_bypass_phase1.py <RUN_ID>")
        sys.exit(1)

    run_id = sys.argv[1]

    root = Path("C:/Users/kenne/OneDrive/Documentos/worqai-marketing")
    db = Database(root / ".quantum" / "control.db")
    repo = Repository(db, initialize=False)
    sm = StateMachine(repo)

    # Get current run status
    run = repo.require(Run, run_id)
    print(f"[1] Current status: {run.status.value} (state_version: {run.state_version})")

    spec = repo.require(SpecVersion, run.active_spec_version_id)
    base_sha = run.metadata.get("base_sha") or _git(root, "rev-parse", "HEAD")
    print(f"[2] Base SHA: {base_sha}")

    # --- CREATE PLAN ---
    plan_content = {
        "tasks": [
            {
                "id": "reframe-carousels",
                "title": "Reframe Batch carousels with WorqAI lime identity",
                "description": (
                    "Reframe carousel HTML files for WorqAI marketing with dark lime identity (#C7FF3A), "
                    "unified CTAs, and excellent contrast. Apply light/dark theme split per spec. "
                    "Ensure no overlap, proper contrast, unified CTA design, worqai.io branding, and html2canvas-safe CSS. "
                    "Save all outputs to production/Carousels to remake/priority 1/Batch X/reframed/"
                ),
                "allowed_paths": ["production/Carousels to remake/priority 1/Batch X/reframed/"],
                "validation": ["ls production/Carousels to remake/priority 1/Batch X/reframed/"]
            }
        ],
        "edges": [],
        "base_sha": base_sha,
        "open_decisions": [],
        "risks": []
    }

    plan = repo.create_plan_version(run_id, spec.id, plan_content)
    print(f"[3] Created plan: {plan.id}")

    # --- CREATE TASK ---
    task = repo.add(
        Task(
            id=f"{plan.id[:12]}-reframe-carousels",
            run_id=run_id,
            plan_version_id=plan.id,
            title="Reframe Batch carousels with WorqAI lime identity",
            description=plan_content["tasks"][0]["description"],
            metadata={
                "base_sha": base_sha,
                "allowed_paths": plan_content["tasks"][0]["allowed_paths"],
                "validation": plan_content["tasks"][0]["validation"],
            },
        )
    )
    print(f"[4] Created task: {task.id}")

    # --- TRANSITION: spec_approval → planning → plan_decisions → plan_approval ---
    transitions = [
        (RunStatus.PLANNING, "planning"),
        (RunStatus.PLAN_DECISIONS, "plan_decisions"),
        (RunStatus.PLAN_APPROVAL, "plan_approval"),
    ]

    for target_status, label in transitions:
        run = repo.require(Run, run_id)
        try:
            run = sm.transition_run(run_id, target_status, run.state_version, actor="human-manual")
            print(f"[5] Transitioned to: {run.status.value}")
        except Exception as e:
            print(f"[5] Transition to {label} failed or skipped: {e}")
            # Continue — state might already be there

    # --- CREATE APPROVAL ---
    run = repo.require(Run, run_id)
    approval = repo.add(
        Approval(
            run_id=run_id,
            scope="plan",
            target_id=plan.id,
            subject_hash=plan.content_hash,
            status=ApprovalStatus.APPROVED,
            decided_by="human-manual",
            decided_at=datetime.now(timezone.utc),
            reason="Manual bypass due to Claude CLI session limit"
        )
    )
    print(f"[6] Created approval: {approval.id}")

    # --- TRANSITION: plan_approval → ready ---
    run = repo.require(Run, run_id)
    run = sm.transition_run(run_id, RunStatus.READY, run.state_version, actor="human-manual")
    print(f"[7] Transitioned to: {run.status.value}")

    # --- CREATE GIT WORKTREE ---
    manager = GitWorktreeManager(root)
    worktree = manager.create(f"{run_id[:8]}-reframe-carousels", base=base_sha)
    print(f"[8] Created worktree: {worktree.path}")
    print(f"    Branch: {worktree.branch}")

    # --- UPDATE METADATA ---
    run = repo.require(Run, run_id)
    metadata = dict(run.metadata)
    metadata.update(
        candidate_worktree=str(worktree.path),
        candidate_branch=worktree.branch,
        base_sha=base_sha,
    )
    run = repo.update_versioned(Run, run_id, run.state_version, {"metadata": metadata})
    print(f"[9] Updated metadata with worktree info")

    # --- WRITE PROJECTIONS ---
    from quantum_v4.control_plane import ControlPlane
    from quantum_v4.providers import ClaudeCliProvider
    cp = ControlPlane(repo, root, ClaudeCliProvider())
    cp._write_projections(run_id)
    print(f"[10] Wrote projections")

    print(f"\n{'='*50}")
    print(f"Run ID: {run_id}")
    print(f"Status: {run.status.value}")
    print(f"Task ID: {task.id}")
    print(f"Plan ID: {plan.id}")
    print(f"Worktree: {worktree.path}")
    print(f"\nNEXT: Build the carousel files in the worktree.")
    print(f"Then run: python quantum_bypass_phase2.py {run_id}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
