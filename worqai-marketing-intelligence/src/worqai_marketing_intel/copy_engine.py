"""Request-sensitive copy primitives shared by WMI engines."""

from __future__ import annotations

import re

from .models import MarketingTask


def strategic_angle(task: MarketingTask) -> str:
    topic = clean_topic(task.topic)
    if is_spanish(task):
        return (
            f"Presentar {topic} como un problema de evidencia y alineación para {task.audience}, "
            f"mostrar el mecanismo de WorqAI y conducir hacia {task.objective}."
        )
    return (
        f"Frame {topic} as an evidence and fit problem for {task.audience}, show the WorqAI "
        f"mechanism, and move the reader toward {task.objective}."
    )


def hooks(task: MarketingTask) -> tuple[str, ...]:
    topic = clean_topic(task.topic)
    audience = audience_label(task.audience, spanish=is_spanish(task))
    if is_spanish(task):
        return (
            f"El problema con {topic} no siempre es falta de experiencia. A menudo es que la evidencia correcta no aparece.",
            f"Si {audience} tienen que explicar mentalmente por qué encajan, el CV ya les está pidiendo demasiado.",
            f"La vacante ya dice qué demostrar. {topic.capitalize()} debería hacer esa evidencia imposible de ignorar.",
        )
    return (
        f"The problem with {topic} is not always missing experience. It is often missing visible evidence.",
        f"If {audience} must mentally reconstruct the fit, the application is already asking too much of them.",
        f"The vacancy already says what to prove. {topic.capitalize()} should make that proof impossible to miss.",
    )


def cta(task: MarketingTask) -> str:
    if is_spanish(task):
        if "partnership" in task.objective:
            return "CTA: Proponga un piloto pequeño con una cohorte, vacantes reales y un ejemplo antes/después."
        if "conversion" in task.objective:
            return "CTA: Pruebe WorqAI con una vacante real y revise la alineación antes de enviar su CV."
        if task.asset_type.value in {"carousel", "linkedin_post", "ig_reel"}:
            return "CTA: Compare hoy su CV con una vacante real en worqai.io."
        return "CTA: Empiece con una vacante y convierta sus requisitos en una estrategia clara para su CV."
    if "partnership" in task.objective:
        return "CTA: Propose a small pilot using one cohort, real roles, and a before/after proof sample."
    if "conversion" in task.objective:
        return "CTA: Test WorqAI with one real vacancy before sending the application."
    return "CTA: Compare one target job description against the current CV in WorqAI."


def proof_line(task: MarketingTask) -> str:
    topic = clean_topic(task.topic)
    if is_spanish(task):
        return (
            f"Muestre {topic} con una vacante real: requisito, evidencia actual, hueco y versión adaptada sin inventar experiencia."
        )
    return (
        f"Demonstrate {topic} with a real role: requirement, current evidence, gap, and truthful adapted version."
    )


def clean_topic(topic: str) -> str:
    cleaned = re.sub(r"\s+", " ", topic).strip(" .:-")
    return cleaned or "role-specific CV applications"


def audience_label(audience: str, *, spanish: bool) -> str:
    lowered = audience.lower()
    if "univers" in lowered or "career center" in lowered:
        return "los equipos de empleabilidad" if spanish else "career teams"
    if "compan" in lowered or "hr" in lowered:
        return "los equipos de recursos humanos" if spanish else "HR teams"
    if "student" in lowered or "early-career" in lowered:
        return "las personas que buscan su primer empleo" if spanish else "early-career candidates"
    if "senior" in lowered or "experienced" in lowered:
        return "los profesionales con experiencia" if spanish else "experienced professionals"
    return "las personas reclutadoras" if spanish else "recruiters"


def is_spanish(task: MarketingTask) -> bool:
    return task.language.lower().startswith("es")
