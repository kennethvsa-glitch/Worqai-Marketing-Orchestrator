"""Plain-language prompt dispatcher for WMI sessions."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from .campaign_package_engine import build_campaign_package
from .codec import to_plain
from .deep_research_engine import build_deep_research_plan
from .feedback_engine import ParsedMetric, build_feedback_loop, parse_metrics
from .memory_store import MemoryStore
from .message_reply_engine import build_message_reply
from .models import AssetType, MarketingTask
from .motion_handoff_engine import build_motion_handoff
from .orchestrator import MarketingOrchestrator
from .router import classify, has_phrase, normalize_text
from .seo_engine import build_seo_plan
from .social_reframe_engine import reframe_social_post
from .universal_intake_engine import execute_universal_intake


@dataclass(frozen=True)
class PromptRuntimeResult:
    mode: str
    request: str
    payload: dict[str, Any]
    notes: tuple[str, ...] = ()


def run_prompt(
    prompt: str,
    *,
    orchestrator: MarketingOrchestrator | None = None,
    save: bool = False,
    live_research: bool = False,
    limit: int = 5,
    _intake_guard: bool = False,
    _forced_mode: str | None = None,
) -> PromptRuntimeResult:
    """Route a natural WMI prompt to one engine and return its output."""

    normalized = normalize_text(prompt)

    # Keep replies ahead of orchestration; this is the latency-sensitive path.
    if _looks_like_message_reply(prompt, normalized):
        request, message = _split_message_prompt(prompt)
        return PromptRuntimeResult(
            mode="message_reply",
            request=request,
            payload=build_message_reply(request, message),
            notes=("Triggered fast reply engine before loading the full orchestrator.",),
        )

    if _forced_mode is not None:
        return _execute_forced_mode(
            _forced_mode,
            prompt,
            orchestrator=orchestrator,
            save=save,
            live_research=live_research,
            limit=limit,
        )

    if _looks_like_social_reframe(normalized):
        request, post = _split_social_post_prompt(prompt)
        return PromptRuntimeResult(
            mode="social_reframe",
            request=request,
            payload=reframe_social_post(request, post),
            notes=("Triggered social reframe because the prompt asks to rewrite a social post.",),
        )

    if _looks_like_script_audit(normalized, prompt):
        request, script = _split_script_prompt(prompt)
        engine = orchestrator or MarketingOrchestrator()
        return PromptRuntimeResult(
            mode="script_audit",
            request=request,
            payload=engine.audit_script(request, script),
            notes=("Triggered script audit because the prompt asks to audit a reel or video script.",),
        )

    task = classify(prompt)

    parsed_metrics = parse_metrics(prompt)
    if parsed_metrics and (
        _looks_like_performance_update(normalized) or _performance_asset_id(prompt)
    ):
        return _performance_update_result(
            task,
            prompt,
            parsed_metrics,
            save=save,
        )

    if _looks_like_action_plan(normalized):
        return _action_plan_result(prompt, orchestrator=orchestrator, save=save)

    specialized = _specialized_result(task, prompt)
    if specialized is not None:
        return specialized

    if task.asset_type == AssetType.RESEARCH:
        return _research_result(
            task,
            prompt,
            orchestrator=orchestrator,
            save=save,
            live_research=live_research,
            limit=limit,
        )

    if task.signals:
        return _brief_result(
            prompt,
            orchestrator=orchestrator,
            save=save,
            live_research=live_research,
            limit=limit,
        )

    if _intake_guard:
        return _brief_result(
            prompt,
            orchestrator=orchestrator,
            save=save,
            live_research=live_research,
            limit=limit,
            notes=("Universal intake recursion guard used the default campaign brief.",),
        )

    decision, inferred = execute_universal_intake(
        prompt,
        lambda mode: run_prompt(
            prompt,
            orchestrator=orchestrator,
            save=save,
            live_research=live_research,
            limit=limit,
            _intake_guard=True,
            _forced_mode=mode,
        ),
    )
    payload = dict(inferred.payload)
    payload["intake_decision"] = decision
    return PromptRuntimeResult(
        mode=inferred.mode,
        request=inferred.request,
        payload=payload,
        notes=inferred.notes + (
            f"Universal intake inferred `{decision['best_mode']}` and executed it once.",
        ),
    )


def _specialized_result(
    task: MarketingTask,
    prompt: str,
) -> PromptRuntimeResult | None:
    builders: dict[AssetType, tuple[str, Any, str]] = {
        AssetType.CAMPAIGN_PACKAGE: (
            "campaign_package",
            build_campaign_package,
            "Triggered campaign package from explicit complete-campaign signals.",
        ),
        AssetType.FEEDBACK_LOOP: (
            "feedback_loop",
            build_feedback_loop,
            "Triggered feedback engine from performance-learning signals.",
        ),
        AssetType.MOTION_HANDOFF: (
            "motion_handoff",
            build_motion_handoff,
            "Triggered Motion Studio handoff from render or manifest signals.",
        ),
        AssetType.DEEP_RESEARCH: (
            "deep_research",
            build_deep_research_plan,
            "Triggered deep research from explicit competitor or source-study signals.",
        ),
        AssetType.SEO_PAGE: (
            "seo_plan",
            build_seo_plan,
            "Triggered SEO engine from explicit SEO, ranking, or Google signals.",
        ),
    }
    selected = builders.get(task.asset_type)
    if selected is None:
        return None
    mode, builder, note = selected
    return PromptRuntimeResult(mode=mode, request=prompt, payload=builder(prompt), notes=(note,))


def _brief_result(
    prompt: str,
    *,
    orchestrator: MarketingOrchestrator | None,
    save: bool,
    live_research: bool,
    limit: int,
    notes: tuple[str, ...] = ("Triggered marketing brief generation from detected asset signals.",),
) -> PromptRuntimeResult:
    engine = orchestrator or MarketingOrchestrator()
    brief = engine.brief(prompt)
    payload = to_plain(brief)
    if brief.task.research_requested:
        payload["research_enrichment"] = _research_enrichment(
            engine,
            brief,
            prompt,
            save=save,
            live_research=live_research,
            limit=limit,
        )
        notes += ("Research intent enriched the requested asset without replacing it.",)
    if save:
        payload["memory_id"] = MemoryStore().save_brief(brief)
    return PromptRuntimeResult(mode="brief", request=prompt, payload=payload, notes=notes)


def _research_enrichment(
    engine: MarketingOrchestrator,
    brief: Any,
    prompt: str,
    *,
    save: bool,
    live_research: bool,
    limit: int,
) -> dict[str, Any]:
    store = MemoryStore()
    data: dict[str, Any] = {
        "asset_type": brief.task.asset_type.value,
        "benchmark_patterns": to_plain(brief.benchmark_patterns),
        "saved_examples": [
            to_plain(example)
            for example in store.list_benchmark_examples(
                asset_type=brief.task.asset_type.value,
                limit=limit,
            )
        ],
    }
    normalized = normalize_text(prompt)
    if live_research or _phrase_any(normalized, ("live research", "source backed")):
        report = engine.live_research(prompt, limit=limit)
        data["live_report"] = to_plain(report)
        if save:
            data["saved_live_example_ids"] = _save_live_patterns(store, report)
    return data


def _research_result(
    task: MarketingTask,
    prompt: str,
    *,
    orchestrator: MarketingOrchestrator | None,
    save: bool,
    live_research: bool,
    limit: int,
) -> PromptRuntimeResult:
    engine = orchestrator or MarketingOrchestrator()
    target = str(task.metadata.get("referenced_asset_type") or "campaign")
    target_prompt = f"Create a {target.replace('_', ' ')} based on this research request: {prompt}"
    brief = engine.brief(target_prompt)
    data = _research_enrichment(
        engine,
        brief,
        target_prompt,
        save=save,
        live_research=live_research,
        limit=limit,
    )
    return PromptRuntimeResult(
        mode="research",
        request=prompt,
        payload=data,
        notes=("Triggered research because the prompt asks for examples or benchmarks as its main output.",),
    )


def _save_live_patterns(store: MemoryStore, report: Any) -> list[str]:
    return [
        store.save_benchmark_example(
            asset_type=pattern.asset_type,
            title=pattern.title,
            source=pattern.source,
            pattern=pattern.pattern,
            notes=pattern.notes,
        )
        for pattern in report.extracted_patterns
    ]


def _action_plan_result(
    prompt: str,
    *,
    orchestrator: MarketingOrchestrator | None,
    save: bool,
) -> PromptRuntimeResult:
    engine = orchestrator or MarketingOrchestrator()
    brief, plan = engine.action_plan(prompt)
    payload = to_plain(plan)
    if save:
        payload["plan_id"] = MemoryStore().save_action_plan(plan, brief)
    return PromptRuntimeResult(
        mode="action_plan",
        request=prompt,
        payload=payload,
        notes=("Triggered action planning because the prompt asks where or how to produce the asset.",),
    )


def _performance_update_result(
    task: MarketingTask,
    prompt: str,
    metrics: tuple[ParsedMetric, ...],
    *,
    save: bool,
) -> PromptRuntimeResult:
    asset_id = _performance_asset_id(prompt)
    asset_type = _performance_asset_type(task, prompt)
    channel = _performance_channel(prompt, asset_type)
    context = {
        "asset_id": asset_id,
        "asset_type": asset_type,
        "channel": channel,
    }
    missing_fields = [name for name, value in context.items() if not value]
    saved_ids: tuple[str, ...] = ()
    if save and not missing_fields:
        saved_ids = MemoryStore().save_performance_text(
            asset_id=asset_id,
            asset_type=asset_type,
            channel=channel,
            text=prompt,
        )

    if saved_ids:
        status = "saved"
    elif save and missing_fields:
        status = "not_saved_missing_fields"
    else:
        status = "preview"
    payload: dict[str, Any] = {
        "format": "performance update",
        **context,
        "metrics": [to_plain(metric) for metric in metrics],
        "missing_fields": missing_fields,
        "save_requested": save,
        "saved": bool(saved_ids),
        "saved_event_ids": list(saved_ids),
        "status": status,
        "source_request": prompt,
    }
    note = (
        "Parsed and saved the natural-language performance update."
        if saved_ids
        else "Parsed a performance preview; persistence requires save=True and complete asset context."
    )
    return PromptRuntimeResult(
        mode="performance_update",
        request=prompt,
        payload=payload,
        notes=(note,),
    )


def _execute_forced_mode(
    mode: str,
    prompt: str,
    *,
    orchestrator: MarketingOrchestrator | None,
    save: bool,
    live_research: bool,
    limit: int,
) -> PromptRuntimeResult:
    if mode == "campaign_package":
        return PromptRuntimeResult(mode=mode, request=prompt, payload=build_campaign_package(prompt))
    if mode == "feedback_loop":
        return PromptRuntimeResult(mode=mode, request=prompt, payload=build_feedback_loop(prompt))
    if mode == "motion_handoff":
        return PromptRuntimeResult(mode=mode, request=prompt, payload=build_motion_handoff(prompt))
    if mode == "deep_research":
        return PromptRuntimeResult(mode=mode, request=prompt, payload=build_deep_research_plan(prompt))
    if mode == "seo_plan":
        return PromptRuntimeResult(mode=mode, request=prompt, payload=build_seo_plan(prompt))
    if mode == "social_reframe":
        request, post = _split_social_post_prompt(prompt)
        return PromptRuntimeResult(mode=mode, request=request, payload=reframe_social_post(request, post))
    if mode == "script_audit":
        request, script = _split_script_prompt(prompt)
        engine = orchestrator or MarketingOrchestrator()
        return PromptRuntimeResult(mode=mode, request=request, payload=engine.audit_script(request, script))
    if mode == "message_reply":
        request, message = _split_message_prompt(prompt)
        return PromptRuntimeResult(mode=mode, request=request, payload=build_message_reply(request, message))
    if mode == "research":
        return _research_result(
            classify(prompt),
            prompt,
            orchestrator=orchestrator,
            save=save,
            live_research=live_research,
            limit=limit,
        )
    if mode == "action_plan":
        return _action_plan_result(prompt, orchestrator=orchestrator, save=save)
    return _brief_result(
        prompt,
        orchestrator=orchestrator,
        save=save,
        live_research=live_research,
        limit=limit,
        notes=("Universal intake selected the default marketing brief.",),
    )


def _looks_like_script_audit(normalized: str, prompt: str) -> bool:
    audit_words = ("audit", "review", "rewrite", "improve", "mejora", "mejorar", "revisar", "audita")
    script_words = ("script", "guion", "reel", "video")
    pasted_length = len(prompt.split()) > 80 or "\n\n" in prompt
    return _phrase_any(normalized, audit_words) and (
        _phrase_any(normalized, script_words) or pasted_length
    )


def _looks_like_message_reply(prompt: str, normalized: str) -> bool:
    explicit_phrases = (
        "reply to this message", "reply to this comment", "respond to this message",
        "respond to this comment", "answer this message", "answer this comment",
        "responde a este mensaje", "responde este mensaje", "responde a este comentario",
        "contesta este mensaje", "contesta este comentario",
    )
    if _phrase_any(normalized, explicit_phrases):
        return True
    reply_words = ("reply", "respond", "answer", "contestar", "contesta", "respuesta", "responder", "responde")
    source_markers = ("message:", "comment:", "dm:", "mensaje:", "comentario:")
    return _phrase_any(normalized, reply_words) and any(marker in prompt.casefold() for marker in source_markers)


def _looks_like_social_reframe(normalized: str) -> bool:
    rewrite_words = ("rewrite", "reframe", "improve", "mejora", "mejorar", "revisar", "adapt", "adapta")
    social_words = ("linkedin", "group", "grupo", "post", "job seekers", "buscando brete")
    return _phrase_any(normalized, rewrite_words) and _phrase_any(normalized, social_words)


def _looks_like_action_plan(normalized: str) -> bool:
    return _phrase_any(
        normalized,
        (
            "action plan", "where is it located", "where to put", "prepare production",
            "production plan", "build this in", "create files", "plan de accion",
            "donde guardarlo", "prepara produccion",
        ),
    )


def _looks_like_performance_update(normalized: str) -> bool:
    return _phrase_any(
        normalized,
        (
            "got", "had", "received", "generated", "reached", "performed", "results",
            "performance update", "obtuvo", "recibio", "genero", "alcanzo",
            "tuvo", "consiguio", "logro", "resultados", "rendimiento",
        ),
    )


def _performance_asset_id(prompt: str) -> str:
    patterns = (
        r"\basset[ _-]?id\s*(?:is|es|[:=#])?\s*([A-Za-z0-9][A-Za-z0-9._-]{2,})",
        r"\b(?:for|para)\s+asset\s+([A-Za-z0-9][A-Za-z0-9._-]{2,})",
        r"\b(?:asset|pieza|activo)\s+#?([A-Za-z0-9][A-Za-z0-9._-]{2,})",
        r"#?\b((?:carousel|carrusel|reel|post|video|email|correo|ad|campaign|campana|seo)[-_][A-Za-z0-9._-]+)\b",
    )
    for pattern in patterns:
        match = re.search(pattern, prompt, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip(".,;:")
    return ""


def _performance_asset_type(task: MarketingTask, prompt: str) -> str:
    normalized = normalize_text(prompt)
    type_phrases: tuple[tuple[AssetType, tuple[str, ...]], ...] = (
        (AssetType.CAROUSEL, ("carousel", "carrusel")),
        (AssetType.IG_REEL, ("ig reel", "instagram reel", "reel", "guion")),
        (AssetType.LINKEDIN_POST, ("linkedin post", "post de linkedin", "post")),
        (AssetType.SEO_PAGE, ("seo page", "pagina seo")),
        (AssetType.LANDING_PAGE, ("landing page", "landing", "pagina de aterrizaje")),
        (AssetType.EMAIL, ("email", "correo")),
        (AssetType.AD, ("ad", "ads", "anuncio")),
        (AssetType.MOTION_VIDEO, ("motion video", "video")),
        (AssetType.PARTNERSHIP_PITCH, ("pitch", "propuesta")),
        (AssetType.CAMPAIGN, ("campaign", "campana")),
    )
    for asset_type, phrases in type_phrases:
        if _phrase_any(normalized, phrases):
            return asset_type.value
    if task.signals and task.asset_type not in {
        AssetType.FEEDBACK_LOOP,
        AssetType.RESEARCH,
        AssetType.DEEP_RESEARCH,
    }:
        return task.asset_type.value
    return ""


def _performance_channel(prompt: str, asset_type: str) -> str:
    normalized = normalize_text(prompt)
    channels = (
        (("linkedin", "instagram", "tiktok", "social", "redes sociales"), "social"),
        (("google", "search", "seo", "busqueda"), "seo"),
        (("email", "correo", "outreach", "whatsapp", "dm"), "outreach"),
        (("product", "producto", "in app"), "product"),
    )
    for phrases, channel in channels:
        if _phrase_any(normalized, phrases):
            return channel
    defaults = {
        AssetType.CAROUSEL.value: "social",
        AssetType.IG_REEL.value: "social",
        AssetType.LINKEDIN_POST.value: "social",
        AssetType.AD.value: "social",
        AssetType.MOTION_VIDEO.value: "social",
        AssetType.SEO_PAGE.value: "seo",
        AssetType.LANDING_PAGE.value: "seo",
        AssetType.EMAIL.value: "outreach",
        AssetType.PARTNERSHIP_PITCH.value: "outreach",
        AssetType.MESSAGE_REPLY.value: "outreach",
    }
    return defaults.get(asset_type, "")


def _phrase_any(text: str, phrases: tuple[str, ...]) -> bool:
    return any(has_phrase(text, phrase) for phrase in phrases)


def _split_script_prompt(prompt: str) -> tuple[str, str]:
    if "|" in prompt:
        request, script = [part.strip() for part in prompt.split("|", maxsplit=1)]
        if request and script:
            return request, script

    lowered = prompt.casefold()
    for marker in ("script:", "guion:", "guión:", "copy:", "texto:"):
        index = lowered.find(marker)
        if index >= 0:
            request = prompt[:index].strip(" :-") or "Audit and improve this WorqAI reel script"
            script = prompt[index + len(marker):].strip()
            if script:
                return request, script

    if ":" in prompt:
        request, script = [part.strip() for part in prompt.split(":", maxsplit=1)]
        normalized_request = normalize_text(request)
        if script and _phrase_any(
            normalized_request,
            ("audit", "review", "rewrite", "improve", "mejora", "mejorar"),
        ) and _phrase_any(normalized_request, ("script", "guion", "reel", "video")):
            return request or "Audit and improve this WorqAI reel script", script

    return "Audit and improve a Spanish IG reel script for WorqAI", prompt


def _split_social_post_prompt(prompt: str) -> tuple[str, str]:
    lowered = prompt.casefold()
    for marker in ("post:", "texto:", "copy:"):
        index = lowered.find(marker)
        if index >= 0:
            request = prompt[:index].strip(" :-") or "Reframe this WorqAI social post"
            post = prompt[index + len(marker):].strip()
            if post:
                return request, post
    if ":" in prompt:
        request, post = [part.strip() for part in prompt.split(":", maxsplit=1)]
        if post:
            return request or "Reframe this WorqAI social post", post
    return "Reframe this WorqAI social post", prompt


def _split_message_prompt(prompt: str) -> tuple[str, str]:
    lowered = prompt.casefold()
    for marker in ("message:", "comment:", "dm:", "mensaje:", "comentario:"):
        index = lowered.find(marker)
        if index >= 0:
            request = prompt[:index].strip(" :-") or "Create a WorqAI message reply"
            message = prompt[index + len(marker):].strip()
            if message:
                return request, message
    if ":" in prompt:
        request, message = [part.strip() for part in prompt.split(":", maxsplit=1)]
        if message:
            return request or "Create a WorqAI message reply", message
    return "Create a WorqAI message reply", prompt
