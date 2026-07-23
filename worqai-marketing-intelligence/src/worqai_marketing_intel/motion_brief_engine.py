"""Request-sensitive motion video brief assembly."""

from __future__ import annotations

from .copy_engine import clean_topic, cta, hooks, is_spanish, proof_line
from .models import MarketingTask


def build_motion_brief(task: MarketingTask) -> dict[str, object]:
    topic = clean_topic(task.topic)
    copy = _scene_copy(task, topic)
    timings = ((0, 4), (4, 11), (11, 21), (21, 33), (33, 42))
    scenes = [
        {
            "id": f"s{index:02d}",
            "start_seconds": start,
            "end_seconds": end,
            "purpose": purpose,
            "visual": visual,
            "copy": line,
        }
        for index, ((start, end), (purpose, visual, line)) in enumerate(zip(timings, copy), start=1)
    ]
    return {
        "format": "42-second motion video brief",
        "topic": topic,
        "audience": task.audience,
        "market": task.market,
        "objective": task.objective,
        "concept": hooks(task)[0],
        "scenes": scenes,
        "motion_language": "Precise document movement, requirement-to-evidence mapping, restrained type, and proof-led transitions.",
        "voiceover": " ".join(scene["copy"] for scene in scenes),
        "sound_intent": "One subtle scan pulse, restrained transitions, and a resolved final beat; voice remains primary.",
        "proof_requirement": proof_line(task),
        "cta": cta(task),
        "handoff_requirements": [
            "Map every beat to Motion Studio timeline labels.",
            "Use real or explicitly labeled illustrative product states.",
            "Run scene lint, orthography, safe-zone, contact-sheet, and deterministic export checks.",
        ],
    }


def _scene_copy(task: MarketingTask, topic: str) -> list[tuple[str, str, str]]:
    if is_spanish(task):
        return [
            ("hook", "Una vacante y un CV aparecen desalineados.", hooks(task)[0]),
            ("diagnose", "La vacante se convierte en requisitos verificables.", f"En {topic}, el puesto ya indica qué habilidades, herramientas y resultados necesita encontrar."),
            ("map", "WorqAI conecta cada requisito con evidencia real del CV.", "WorqAI muestra qué ya está demostrado, qué está escondido y qué falta aclarar."),
            ("prove", "Una línea real cambia delante de la audiencia.", "No inventa experiencia. Convierte evidencia dispersa en una versión específica para el puesto."),
            ("act", "CV adaptado, descarga y URL.", cta(task).removeprefix("CTA: ")),
        ]
    return [
        ("hook", "A vacancy and CV appear visibly misaligned.", hooks(task)[0]),
        ("diagnose", "The vacancy becomes verifiable requirements.", f"For {topic}, the role already says which skills, tools, and outcomes it needs to find."),
        ("map", "WorqAI connects each requirement to real CV evidence.", "WorqAI shows what is proven, what is buried, and what still needs clarification."),
        ("prove", "One real line transforms in front of the audience.", "It does not invent experience. It turns scattered evidence into a role-specific version."),
        ("act", "Adapted CV, download, and URL.", cta(task).removeprefix("CTA: ")),
    ]
