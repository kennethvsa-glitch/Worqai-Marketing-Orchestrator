"""Targeted partnership pitch generation."""

from __future__ import annotations

from .copy_engine import clean_topic, is_spanish
from .models import MarketingTask


def build_partnership_pitch(task: MarketingTask) -> dict[str, object]:
    organization = str(task.metadata.get("organization") or "the target organization")
    segment = _segment(task)
    topic = clean_topic(task.topic)
    outcome, pain, pilot = _offer(task, segment)
    return {
        "format": "targeted partnership pitch",
        "organization": organization,
        "segment": segment,
        "market": task.market,
        "topic": topic,
        "stakeholder_outcome": outcome,
        "operational_pain": pain,
        "pilot": pilot,
        "initial_email": _initial_email(task, organization, outcome, pilot),
        "follow_up": _follow_up(task, organization),
        "meeting_talk_track": _talk_track(task, outcome, pilot),
        "proof_to_prepare": [
            f"One before/after example relevant to {segment}.",
            "A real vacancy-to-CV fit-gap sample with invented personal data clearly labeled.",
            "Pilot scope: cohort size, target roles, duration, owner, and success criteria.",
            "A one-page data-handling and no-invention statement.",
        ],
        "success_metrics": [
            "participant completion rate",
            "role-requirement coverage before vs after",
            "advisor or stakeholder usefulness score",
            "qualified interest in continuing after the pilot",
        ],
        "objections": _objections(task),
        "next_step": _next_step(task, organization),
    }


def _segment(task: MarketingTask) -> str:
    audience = task.audience.lower()
    if "univers" in audience or "career center" in audience:
        return "university career and employability team"
    if "compan" in audience or "hr" in audience:
        return "company HR or internal-mobility team"
    if "coach" in audience or "recruit" in audience:
        return "career-services operator"
    return "workforce development program"


def _offer(task: MarketingTask, segment: str) -> tuple[str, str, str]:
    if "university" in segment:
        return (
            "help students translate academic, project, and internship evidence into role-specific applications",
            "career teams cannot manually tailor every student's CV to every vacancy",
            "a 20-student, two-role pilot with a workshop, self-service WorqAI access, and a before/after report",
        )
    if "company" in segment:
        return (
            "make internal-mobility and early-career applications easier to evaluate",
            "relevant internal experience is often buried in generic application language",
            "a 10-25 person pilot around one role family with fit-gap reporting and participant review",
        )
    return (
        "scale role-specific application support without multiplying advisor workload",
        "participants apply across different roles while advisors repeat the same translation work",
        "a bounded cohort pilot using real vacancies, self-service adaptation, and advisor-visible outcomes",
    )


def _initial_email(task: MarketingTask, organization: str, outcome: str, pilot: str) -> dict[str, str]:
    if is_spanish(task):
        return {
            "subject": f"Piloto pequeño de empleabilidad para {organization}",
            "body": (
                f"Hola [Nombre], estoy construyendo WorqAI para ayudar a {outcome}. "
                "La herramienta compara un CV con una vacante real, muestra los huecos de evidencia y ayuda a adaptar "
                "la redacción sin inventar experiencia. En lugar de proponer una implementación grande, me gustaría "
                f"validar {pilot}. ¿Tendría sentido conversar 20 minutos con la persona que lidera empleabilidad o movilidad?"
            ),
        }
    return {
        "subject": f"Small employability pilot for {organization}",
        "body": (
            f"Hi [Name], I am building WorqAI to {outcome}. It compares a CV with a real vacancy, "
            "shows evidence gaps, and helps adapt the wording without inventing experience. Rather than proposing "
            f"a broad rollout, I would like to validate {pilot}. Would a 20-minute conversation with the owner of "
            "employability or internal mobility make sense?"
        ),
    }


def _follow_up(task: MarketingTask, organization: str) -> str:
    if is_spanish(task):
        return f"Puedo enviar a {organization} un ejemplo antes/después y una propuesta de piloto de una página antes de reunirnos."
    return f"I can send {organization} a before/after example and a one-page pilot outline before we meet."


def _talk_track(task: MarketingTask, outcome: str, pilot: str) -> list[str]:
    return [
        "Problem: qualified people often present evidence in language that does not match the target role.",
        "Mechanism: WorqAI maps vacancy requirements to existing CV evidence and visible gaps.",
        "Boundary: it improves translation and structure; it does not invent experience or guarantee outcomes.",
        f"Stakeholder outcome: {outcome}.",
        f"Low-risk validation: {pilot}.",
    ]


def _objections(task: MarketingTask) -> list[dict[str, str]]:
    return [
        {"objection": "We already provide CV support.", "response": "Use WorqAI after general CV support, when each participant must translate the same experience toward a specific vacancy."},
        {"objection": "AI may invent information.", "response": "The pilot requires source-backed edits, participant review, and an explicit no-invention rule."},
        {"objection": "We need evidence first.", "response": "That is why the first ask is a bounded pilot with defined before/after and usefulness measures."},
    ]


def _next_step(task: MarketingTask, organization: str) -> str:
    if is_spanish(task):
        return f"Enviar a {organization} el ejemplo antes/después y acordar una llamada de 20 minutos para delimitar el piloto."
    return f"Send {organization} the before/after proof and book a 20-minute pilot-scoping call."
