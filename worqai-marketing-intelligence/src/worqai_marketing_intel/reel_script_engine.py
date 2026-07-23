"""Request-sensitive Instagram, TikTok, and Shorts concept generation."""

from __future__ import annotations

from .copy_engine import clean_topic, cta, hooks, is_spanish, proof_line
from .models import MarketingTask


def build_reel_script(task: MarketingTask) -> dict[str, object]:
    count = max(1, min(int(task.metadata.get("requested_count", 3)), 5))
    topic = clean_topic(task.topic)
    hook_options = hooks(task)
    concepts = [_concept(task, topic, index, hook_options[index % len(hook_options)]) for index in range(count)]
    return {
        "format": f"{count} short-form video concepts",
        "platforms": [task.channel or "Instagram Reels", "TikTok", "YouTube Shorts"],
        "topic": topic,
        "audience": task.audience,
        "market": task.market,
        "objective": task.objective,
        "concepts": concepts,
        "production_notes": _production_notes(task),
        "research_requested": task.research_requested,
    }


def _concept(task: MarketingTask, topic: str, index: int, hook: str) -> dict[str, object]:
    if is_spanish(task):
        names = ("El hueco visible", "La prueba antes del consejo", "Dos vacantes, dos estrategias")
        scripts = (
            (
                f"{hook} Tome {topic}. Primero, vea qué pide la vacante. Después, busque dónde su CV "
                "demuestra esas habilidades con herramientas, resultados y contexto. Si la evidencia existe "
                "pero está escondida, WorqAI ayuda a hacerla visible sin inventar nada. "
                f"{cta(task).removeprefix('CTA: ')}"
            ),
            (
                f"{hook} No empiece cambiando el diseño. Empiece con una línea real del CV. Compare esa línea "
                f"con lo que exige el puesto y marque lo que falta en {topic}: alcance, resultado o herramienta. "
                "Luego reescriba con evidencia real. Eso es adaptación, no fabricación. "
                f"{cta(task).removeprefix('CTA: ')}"
            ),
            (
                f"{hook} Ponga dos vacantes lado a lado. Aunque ambas parezcan similares, pueden pedir pruebas "
                f"distintas. {topic.capitalize()} cambia cuando cambia el resultado que la empresa necesita. "
                "WorqAI convierte cada descripción en una estrategia específica para el CV. "
                f"{cta(task).removeprefix('CTA: ')}"
            ),
        )
        visuals = (
            "Vacancy requirement -> current CV evidence -> highlighted gap -> adapted line.",
            "One real bullet on screen, diagnostic annotations, then a restrained before/after reveal.",
            "Split screen with two vacancies, different proof tags, and two resulting CV priorities.",
        )
        captions = (
            f"{topic.capitalize()}: haga visible la evidencia que la vacante sí está buscando.",
            "No cambie palabras por cambiar. Muestre mejor la experiencia que ya existe.",
            "La misma experiencia puede necesitar una estrategia distinta para cada puesto.",
        )
    else:
        names = ("The visible gap", "Proof before advice", "Two roles, two strategies")
        scripts = (
            f"{hook} Start with {topic}. Read what the role asks for, then locate where the CV proves it through tools, outcomes, and context. If the evidence exists but is buried, WorqAI helps surface it without inventing anything. {cta(task).removeprefix('CTA: ')}",
            f"{hook} Do not start by changing the design. Put one real CV line beside the role requirement and mark what is missing from {topic}: scope, result, or tool. Rewrite with real evidence. That is adaptation, not fabrication. {cta(task).removeprefix('CTA: ')}",
            f"{hook} Put two vacancies side by side. Similar titles can ask for different proof. {topic.capitalize()} changes when the employer's required outcome changes. WorqAI turns each description into a specific CV strategy. {cta(task).removeprefix('CTA: ')}",
        )
        visuals = (
            "Vacancy requirement -> current CV evidence -> highlighted gap -> adapted line.",
            "One real bullet on screen, diagnostic annotations, then a restrained before/after reveal.",
            "Split screen with two vacancies, different proof tags, and two resulting CV priorities.",
        )
        captions = (
            f"Make the evidence behind {topic} visible to the role.",
            "Do not swap words for the sake of it. Surface the experience that already exists.",
            "The same experience may need a different strategy for each role.",
        )
    variant = index % 3
    return {
        "name": names[variant],
        "hook": hook,
        "spoken_script": scripts[variant],
        "visual_beats": [beat.strip() for beat in visuals[variant].split(" -> ")],
        "proof": proof_line(task),
        "caption": captions[variant],
        "cta": cta(task),
        "estimated_duration_seconds": 35 if variant != 2 else 40,
    }


def _production_notes(task: MarketingTask) -> list[str]:
    notes = [
        "Deliver the consequence in the first three seconds.",
        "Use a real or clearly labeled illustrative vacancy and CV excerpt.",
        "Keep on-screen text inside 9:16 mobile-safe zones.",
        "Show the WorqAI workflow before the final CTA.",
        "Qualify ATS claims and never promise interviews.",
    ]
    notes.extend(task.constraints)
    return notes
