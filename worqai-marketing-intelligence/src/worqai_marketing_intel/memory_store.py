"""SQLite memory for generated marketing work."""

from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from math import fsum
from pathlib import Path
from typing import Any, Iterator

from .codec import to_plain
from .feedback_engine import canonical_metric_name, metric_direction, metric_weight, parse_metrics
from .models import (
    ActionPlanRecord,
    BenchmarkExample,
    MarketingBrief,
    PerformanceEvent,
    WorkspaceActionPlan,
)
from .paths import default_memory_path


@dataclass(frozen=True)
class MemoryRecord:
    id: str
    created_at: str
    request: str
    asset_type: str
    workspace_id: str
    quality_score: int


@dataclass(frozen=True)
class RankedBenchmarkExample:
    """A saved benchmark with deterministic, channel-scoped performance evidence."""

    example: BenchmarkExample
    score: float
    event_count: int
    metrics: tuple[tuple[str, float], ...]
    channels: tuple[str, ...]


class MemoryStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_memory_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def save_brief(self, brief: MarketingBrief) -> str:
        record_id = uuid.uuid4().hex[:12]
        created_at = datetime.now(UTC).isoformat(timespec="seconds")
        payload = to_plain(brief)
        with self._connect() as db:
            db.execute(
                """
                insert into briefs (
                  id, created_at, request, asset_type, workspace_id,
                  quality_score, payload_json
                ) values (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    created_at,
                    brief.task.request,
                    brief.task.asset_type.value,
                    brief.workspace.workspace_id,
                    brief.quality.score,
                    json.dumps(payload, indent=2),
                ),
            )
        return record_id

    def list_briefs(self, limit: int = 10) -> list[MemoryRecord]:
        with self._connect() as db:
            rows = db.execute(
                """
                select id, created_at, request, asset_type, workspace_id, quality_score
                from briefs
                order by created_at desc
                limit ?
                """,
                (limit,),
            ).fetchall()
        return [MemoryRecord(*row) for row in rows]

    def get_brief_payload(self, record_id: str) -> dict[str, Any]:
        with self._connect() as db:
            row = db.execute(
                "select payload_json from briefs where id = ?",
                (record_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"No brief found for id {record_id}")
        return json.loads(row[0])

    def save_action_plan(self, plan: WorkspaceActionPlan, brief: MarketingBrief) -> str:
        record_id = uuid.uuid4().hex[:12]
        created_at = datetime.now(UTC).isoformat(timespec="seconds")
        with self._connect() as db:
            db.execute(
                """
                insert into action_plans (
                  id, created_at, request, workspace_id, asset_type,
                  status, plan_json, brief_json
                ) values (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    created_at,
                    plan.source_request,
                    plan.workspace_id,
                    plan.asset_type,
                    "pending",
                    json.dumps(to_plain(plan), indent=2),
                    json.dumps(to_plain(brief), indent=2),
                ),
            )
        return record_id

    def list_action_plans(self, limit: int = 10) -> list[ActionPlanRecord]:
        with self._connect() as db:
            rows = db.execute(
                """
                select id, created_at, request, workspace_id, asset_type, status
                from action_plans
                order by created_at desc
                limit ?
                """,
                (limit,),
            ).fetchall()
        return [ActionPlanRecord(*row) for row in rows]

    def approve_action_plan(self, plan_id: str) -> None:
        self.update_action_plan_status(plan_id, "approved")

    def update_action_plan_status(self, plan_id: str, status: str) -> None:
        with self._connect() as db:
            cursor = db.execute(
                "update action_plans set status = ? where id = ?",
                (status, plan_id),
            )
        if cursor.rowcount == 0:
            raise KeyError(f"No action plan found for id {plan_id}")

    def get_action_plan_bundle(self, plan_id: str) -> tuple[str, dict[str, Any], dict[str, Any]]:
        with self._connect() as db:
            row = db.execute(
                "select status, plan_json, brief_json from action_plans where id = ?",
                (plan_id,),
            ).fetchone()
        if row is None:
            raise KeyError(f"No action plan found for id {plan_id}")
        return row[0], json.loads(row[1]), json.loads(row[2])

    def save_benchmark_example(
        self,
        *,
        asset_type: str,
        title: str,
        source: str,
        pattern: str,
        notes: str = "",
    ) -> str:
        record_id = uuid.uuid4().hex[:12]
        created_at = datetime.now(UTC).isoformat(timespec="seconds")
        with self._connect() as db:
            db.execute(
                """
                insert into benchmark_examples (
                  id, created_at, asset_type, title, source, pattern, notes
                ) values (?, ?, ?, ?, ?, ?, ?)
                """,
                (record_id, created_at, asset_type, title, source, pattern, notes),
            )
        return record_id

    def list_benchmark_examples(
        self,
        *,
        asset_type: str | None = None,
        limit: int = 10,
    ) -> list[BenchmarkExample]:
        if asset_type:
            query = """
                select id, created_at, asset_type, title, source, pattern, notes
                from benchmark_examples
                where asset_type = ?
                order by created_at desc
                limit ?
            """
            params: tuple[Any, ...] = (asset_type, limit)
        else:
            query = """
                select id, created_at, asset_type, title, source, pattern, notes
                from benchmark_examples
                order by created_at desc
                limit ?
            """
            params = (limit,)
        with self._connect() as db:
            rows = db.execute(query, params).fetchall()
        return [BenchmarkExample(*row) for row in rows]

    def save_performance_event(
        self,
        *,
        asset_id: str,
        asset_type: str,
        channel: str,
        metric_name: str,
        metric_value: float,
        notes: str = "",
    ) -> str:
        record_id = uuid.uuid4().hex[:12]
        created_at = datetime.now(UTC).isoformat(timespec="seconds")
        with self._connect() as db:
            db.execute(
                """
                insert into performance_events (
                  id, created_at, asset_id, asset_type, channel,
                  metric_name, metric_value, notes
                ) values (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record_id,
                    created_at,
                    asset_id,
                    asset_type,
                    channel,
                    metric_name,
                    float(metric_value),
                    notes,
                ),
            )
        return record_id

    def save_performance_text(
        self,
        *,
        asset_id: str,
        asset_type: str,
        channel: str,
        text: str,
        notes: str = "",
    ) -> tuple[str, ...]:
        """Parse a natural-language update and persist each recognized metric."""

        record_ids: list[str] = []
        for metric in parse_metrics(text):
            record_ids.append(
                self.save_performance_event(
                    asset_id=asset_id,
                    asset_type=asset_type,
                    channel=channel,
                    metric_name=metric.name,
                    metric_value=metric.value,
                    notes=notes or metric.original,
                )
            )
        return tuple(record_ids)

    def list_performance_events(
        self,
        *,
        asset_type: str | None = None,
        channel: str | None = None,
        limit: int = 20,
    ) -> list[PerformanceEvent]:
        filters: list[str] = []
        params: list[Any] = []
        if asset_type:
            filters.append("asset_type = ?")
            params.append(asset_type)
        if channel:
            filters.append("channel = ?")
            params.append(channel)
        where = f"where {' and '.join(filters)}" if filters else ""
        params.append(limit)
        with self._connect() as db:
            rows = db.execute(
                f"""
                select id, created_at, asset_id, asset_type, channel,
                       metric_name, metric_value, notes
                from performance_events
                {where}
                order by created_at desc
                limit ?
                """,
                tuple(params),
            ).fetchall()
        return [PerformanceEvent(*row) for row in rows]

    def rank_benchmark_examples(
        self,
        *,
        asset_type: str | None = None,
        channel: str | None = None,
        limit: int = 10,
    ) -> list[RankedBenchmarkExample]:
        """Rank saved examples whose IDs have matching performance events.

        Values are summed per canonical metric, normalized against peers in the
        same query, and combined using stable metric weights. Lower-is-better
        metrics such as average position are inverted before scoring.
        """

        filters: list[str] = []
        params: list[Any] = []
        if asset_type:
            filters.append("b.asset_type = ?")
            params.append(asset_type)
        if channel:
            filters.append("p.channel = ?")
            params.append(channel)
        where = f"where {' and '.join(filters)}" if filters else ""
        with self._connect() as db:
            rows = db.execute(
                f"""
                select b.id, b.created_at, b.asset_type, b.title, b.source,
                       b.pattern, b.notes, p.channel, p.metric_name, p.metric_value
                from benchmark_examples b
                join performance_events p on p.asset_id = b.id
                {where}
                order by b.id asc, p.metric_name asc, p.created_at asc, p.id asc
                """,
                tuple(params),
            ).fetchall()

        examples: dict[str, BenchmarkExample] = {}
        metric_values: dict[str, dict[str, list[float]]] = {}
        event_counts: dict[str, int] = {}
        channels: dict[str, set[str]] = {}
        for row in rows:
            example_id = row[0]
            examples[example_id] = BenchmarkExample(*row[:7])
            metric = canonical_metric_name(row[8])
            metric_values.setdefault(example_id, {}).setdefault(metric, []).append(float(row[9]))
            event_counts[example_id] = event_counts.get(example_id, 0) + 1
            channels.setdefault(example_id, set()).add(row[7])
        if not examples or limit <= 0:
            return []

        totals = {
            example_id: {
                name: fsum(sorted(values))
                for name, values in grouped_values.items()
            }
            for example_id, grouped_values in metric_values.items()
        }
        metric_names = sorted({name for values in totals.values() for name in values})
        denominators = {
            name: max(abs(values.get(name, 0.0)) for values in totals.values())
            for name in metric_names
        }
        total_weight = sum(metric_weight(name) for name in metric_names) or 1.0
        ranked: list[RankedBenchmarkExample] = []
        for example_id, example in examples.items():
            weighted_score = 0.0
            for name in metric_names:
                value = totals[example_id].get(name)
                if value is None:
                    continue
                peer_values = [values[name] for values in totals.values() if name in values]
                if metric_direction(name) == "lower":
                    positive = [peer for peer in peer_values if peer > 0]
                    normalized = min(positive) / value if positive and value > 0 else 0.0
                else:
                    denominator = denominators[name]
                    normalized = max(0.0, value / denominator) if denominator else 0.0
                weighted_score += min(normalized, 1.0) * metric_weight(name)
            ranked.append(
                RankedBenchmarkExample(
                    example=example,
                    score=round(weighted_score / total_weight, 6),
                    event_count=event_counts[example_id],
                    metrics=tuple(sorted(totals[example_id].items())),
                    channels=tuple(sorted(channels[example_id])),
                )
            )
        ranked.sort(
            key=lambda item: (
                -item.score,
                -item.event_count,
                item.example.title.casefold(),
                item.example.source,
                item.example.pattern,
                item.example.id,
            )
        )
        return ranked[:limit]

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        db = sqlite3.connect(self.path)
        try:
            yield db
            db.commit()
        finally:
            db.close()

    def _init(self) -> None:
        with self._connect() as db:
            db.execute(
                """
                create table if not exists briefs (
                  id text primary key,
                  created_at text not null,
                  request text not null,
                  asset_type text not null,
                  workspace_id text not null,
                  quality_score integer not null,
                  payload_json text not null
                )
                """
            )
            db.execute(
                """
                create table if not exists action_plans (
                  id text primary key,
                  created_at text not null,
                  request text not null,
                  workspace_id text not null,
                  asset_type text not null,
                  status text not null,
                  plan_json text not null,
                  brief_json text not null
                )
                """
            )
            db.execute(
                """
                create table if not exists benchmark_examples (
                  id text primary key,
                  created_at text not null,
                  asset_type text not null,
                  title text not null,
                  source text not null,
                  pattern text not null,
                  notes text not null default ''
                )
                """
            )
            db.execute(
                """
                create table if not exists performance_events (
                  id text primary key,
                  created_at text not null,
                  asset_id text not null,
                  asset_type text not null,
                  channel text not null,
                  metric_name text not null,
                  metric_value real not null,
                  notes text not null default ''
                )
                """
            )
