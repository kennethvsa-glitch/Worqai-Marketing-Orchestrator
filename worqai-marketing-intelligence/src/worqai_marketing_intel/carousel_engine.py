"""Request-sensitive carousel concept assembly."""

from __future__ import annotations

import re

from .copy_engine import clean_topic, cta, hooks, is_spanish, proof_line
from .models import MarketingTask


def build_carousel(task: MarketingTask) -> dict[str, object]:
    topic = clean_topic(task.topic)
    slide_count = _slide_count(task)
    selected_hooks = hooks(task)
    slides = _slides(task, topic, slide_count, selected_hooks[0])
    return {
        "format": f"{slide_count}-slide carousel",
        "channel": task.channel,
        "topic": topic,
        "audience": task.audience,
        "market": task.market,
        "objective": task.objective,
        "hook_options": selected_hooks,
        "recommended_hook": selected_hooks[0],
        "slides": slides,
        "visual_direction": _visual_direction(task),
        "caption": _caption(task, topic),
        "proof_requirement": proof_line(task),
        "research_requested": task.research_requested,
    }


def _slides(task: MarketingTask, topic: str, count: int, hook: str) -> list[dict[str, object]]:
    if is_spanish(task):
        core = [
            ("hook", hook, "Contraste fuerte, máximo dos bloques de texto."),
            ("tension", f"{topic.capitalize()} falla cuando el CV obliga a la persona reclutadora a reconstruir la conexión con el puesto.", "CV y vacante separados por un hueco visible."),
            ("diagnosis", "Lea la descripción como una lista de pruebas: habilidades, herramientas, resultados, alcance y contexto.", "Requisitos convertidos en etiquetas verificables."),
            ("mechanism", "WorqAI compara esas pruebas con la experiencia que ya aparece en el CV.", "Interfaz de comparación, no ilustración abstracta."),
            ("proof", f"Ejemplo de {topic}: requisito -> línea actual -> evidencia ausente -> versión adaptada.", "Antes/después con anotaciones y cambios resaltados."),
            ("trust", "Adaptar no es inventar. Es hacer explícita la experiencia real que responde a la vacante.", "Sello visual: experiencia real, lenguaje específico."),
            ("action", "Antes de enviar, revise si la parte superior del CV responde a las tres prioridades principales del puesto.", "Checklist de tres puntos."),
            ("cta", cta(task).removeprefix("CTA: "), "Producto real, URL y una sola acción."),
        ]
    else:
        core = [
            ("hook", hook, "Strong contrast, no more than two text blocks."),
            ("tension", f"{topic.capitalize()} fails when the CV makes the recruiter reconstruct the connection to the role.", "CV and vacancy separated by a visible gap."),
            ("diagnosis", "Read the description as a proof list: skills, tools, outcomes, scope, and context.", "Requirements become verifiable tags."),
            ("mechanism", "WorqAI compares that proof with the experience already visible in the CV.", "Show the comparison interface, not an abstract illustration."),
            ("proof", f"Example for {topic}: requirement -> current line -> missing evidence -> adapted version.", "Annotated before/after with highlighted changes."),
            ("trust", "Tailoring is not inventing. It makes real experience explicit for the vacancy.", "Visual trust marker: real experience, specific language."),
            ("action", "Before sending, check whether the top of the CV answers the role's three main priorities.", "Three-item checklist."),
            ("cta", cta(task).removeprefix("CTA: "), "Real product, URL, and one action."),
        ]
    if count <= len(core):
        chosen = core[: max(count - 1, 1)] + [core[-1]]
    else:
        extras = [
            ("objection", "What if the experience is relevant but uses different language? Translate the evidence, not the facts.", "Two equivalent phrases connected by an evidence marker."),
            ("check", "Remove anything the vacancy does not need from the first scan.", "Priority stack with lower-value details muted."),
        ]
        chosen = core[:-1] + extras[: count - len(core)] + [core[-1]]
    return [
        {"number": index, "role": role, "copy": copy, "visual": visual}
        for index, (role, copy, visual) in enumerate(chosen, start=1)
    ]


def _slide_count(task: MarketingTask) -> int:
    for constraint in task.constraints:
        match = re.search(r"exactly (\d+) slides", constraint)
        if match:
            return max(5, min(int(match.group(1)), 10))
    return 8


def _visual_direction(task: MarketingTask) -> dict[str, object]:
    return {
        "system": "diagnostic editorial UI with document evidence",
        "palette": "WorqAI brand colors plus neutral document surfaces and one evidence accent",
        "image_policy": "Use real product captures or labeled mock data; avoid generic career stock imagery.",
        "rhythm": "Alternate dense diagnosis slides with spare proof slides.",
        "mobile_rule": "Keep the main claim readable at 1080x1080 without relying on caption text.",
    }


def _caption(task: MarketingTask, topic: str) -> str:
    if is_spanish(task):
        return f"{topic.capitalize()} no se resuelve agregando palabras al azar. Se resuelve mostrando la evidencia que el puesto necesita encontrar. {cta(task).removeprefix('CTA: ')}"
    return f"{topic.capitalize()} is not solved by adding random keywords. It is solved by surfacing the evidence the role needs to find. {cta(task).removeprefix('CTA: ')}"
