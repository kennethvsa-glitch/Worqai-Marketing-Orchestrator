"""Branch-aware execution for approved action plans."""

from __future__ import annotations

from typing import Any

from .git_tools import GitTools
from .models import ProductionResult
from .verification_runner import VerificationRunner
from .workspace_writer import WorkspaceWriter, plan_from_payload


class ExecutionEngine:
    def __init__(self) -> None:
        self.writer = WorkspaceWriter()
        self.verifier = VerificationRunner()

    def execute(
        self,
        *,
        plan_id: str,
        plan_payload: dict[str, Any],
        brief_payload: dict[str, Any],
        dry_run: bool = True,
        create_branch: bool = False,
        verify: bool = False,
        allow_dirty: bool = False,
    ) -> ProductionResult:
        plan = plan_from_payload(plan_payload)
        git = GitTools(plan.workspace_path)
        notes: list[str] = [
            f"Capability adapter: {plan.capability_id} via {plan.adapter}.",
            f"Source format: {plan.source_format}; final output type: {plan.output_format}.",
        ]

        if not dry_run and not plan.human_approval_required:
            return ProductionResult(
                plan_id=plan_id,
                workspace_id=plan.workspace_id,
                destination_path="",
                dry_run=False,
                wrote=False,
                verification_commands=plan.verification_commands,
                notes=tuple(notes + ["Refused a plan that bypasses the approval contract."]),
            )

        if git.is_repo():
            status_before = git.status_short()
            branch_before = git.branch()
            notes.append(f"Git branch before execution: {branch_before or '-'}")
            if status_before:
                notes.append(f"Git workspace has existing changes: {status_before}")
                if not allow_dirty and not dry_run:
                    return ProductionResult(
                        plan_id=plan_id,
                        workspace_id=plan.workspace_id,
                        destination_path="",
                        dry_run=dry_run,
                        wrote=False,
                        verification_commands=plan.verification_commands,
                        notes=tuple(notes + ["Refused to execute because workspace is dirty."]),
                    )
            if create_branch and not dry_run:
                switched = git.switch_or_create(plan.recommended_branch)
                notes.append(f"Branch command: {switched.command} -> {switched.returncode}")
                if switched.returncode != 0:
                    notes.append(switched.stderr)
                    return ProductionResult(
                        plan_id=plan_id,
                        workspace_id=plan.workspace_id,
                        destination_path="",
                        dry_run=dry_run,
                        wrote=False,
                        verification_commands=plan.verification_commands,
                        notes=tuple(notes),
                    )
            elif create_branch:
                notes.append(f"Dry run: would switch/create branch {plan.recommended_branch}.")
        else:
            notes.append("Target workspace is not a Git repository.")

        result = self.writer.write_payload(
            plan_id=plan_id,
            plan=plan,
            brief_payload=brief_payload,
            dry_run=dry_run,
        )
        notes.extend(result.notes)

        if verify and not dry_run and result.wrote:
            verifications = self.verifier.run(plan.workspace_path, plan.verification_commands)
            for item in verifications:
                notes.append(f"Verification: {item.command} -> {item.returncode}")
                if item.stderr:
                    notes.append(item.stderr)
        elif verify and dry_run:
            notes.append("Dry run: would run verification commands.")
        elif verify:
            notes.append("Verification skipped because no source artifact was written.")

        if git.is_repo():
            diff_status = git.status_short()
            notes.append(f"Git status after execution: {diff_status or 'clean'}")

        return ProductionResult(
            plan_id=plan_id,
            workspace_id=result.workspace_id,
            destination_path=result.destination_path,
            dry_run=dry_run,
            wrote=result.wrote,
            verification_commands=result.verification_commands,
            notes=tuple(notes),
        )
