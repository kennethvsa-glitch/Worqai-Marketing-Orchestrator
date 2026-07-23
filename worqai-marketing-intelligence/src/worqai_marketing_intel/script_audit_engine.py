"""Audit and repair pasted reel or video scripts without replacing their subject."""

from __future__ import annotations

import re

from .models import MarketingTask


RISKY_REPLACEMENTS = (
    (r"\btodos hacen lo mismo\b", "muchos siguen principios similares"),
    (r"\bsin importar qué sistema\b", "aunque cada sistema tiene diferencias"),
    (r"\bun humano nunca llega a verlo\b", "puede reducir la posibilidad de que una persona lo revise"),
    (r"\bmuy probable que\b", "puede aumentar la posibilidad de que"),
    (r"\bsiempre\b", "a menudo"),
    (r"\bgarantizad[oa]\b", "posible"),
)


def audit_script(task: MarketingTask, script: str) -> dict[str, object]:
    cleaned = _clean(script)
    words = re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑ]+\b", cleaned)
    hook = _first_substantial_line(cleaned)
    issues = _issues(cleaned, hook, len(words))
    score = max(10 - sum(int(item["penalty"]) for item in issues), 1)
    rewritten = _rewrite(task, cleaned)
    recommended_hook = _recommended_hook(task, cleaned)
    return {
        "format": "Spanish reel script audit",
        "engine_version": "source-preserving-v2",
        "language": task.language or "es-LatAm",
        "topic": task.topic,
        "word_count": len(words),
        "estimated_duration": _duration(len(words)),
        "score": {"value": score, "max": 10, "label": _score_label(score)},
        "diagnosis": _diagnosis(score, len(words), hook, task.topic),
        "hook_audit": {
            "current_hook": hook,
            "recommended_hook": recommended_hook,
            "reason": "Lead with the consequence or tension already present in the source before explaining context.",
        },
        "issues": issues,
        "source_facts_preserved": _source_facts(cleaned),
        "what_to_keep": _what_to_keep(cleaned),
        "what_to_cut_or_compress": _what_to_cut(cleaned),
        "rewritten_script": rewritten,
        "visual_beats": _visual_beats(task, rewritten),
        "best_line": _best_line(rewritten),
        "cta": _cta(task, cleaned),
    }


def _issues(script: str, hook: str, word_count: int) -> list[dict[str, object]]:
    lowered = script.lower()
    issues: list[dict[str, object]] = []
    if word_count > 230:
        issues.append({"severity": "high", "penalty": 2, "problem": "The script is too long for one clear short-form idea.", "fix": "Reduce to 120-180 words or split it into a series."})
    if not _hook_has_tension(hook):
        issues.append({"severity": "high", "penalty": 2, "problem": "The opening delays the consequence or useful tension.", "fix": "Open with the strongest existing consequence, question, or contradiction."})
    risky = [pattern for pattern, _ in RISKY_REPLACEMENTS if re.search(pattern, lowered)]
    if risky:
        issues.append({"severity": "medium", "penalty": 1, "problem": "The script contains absolute or weakly supportable claims.", "examples": risky, "fix": "Qualify the claim without removing its practical meaning."})
    if any(word in lowered for word in ("worqai", "ats", "cv")) and "invent" not in lowered:
        issues.append({"severity": "medium", "penalty": 1, "problem": "The AI/no-invention boundary is missing.", "fix": "State that the tool adapts real experience and requires final review."})
    if not any(word in lowered for word in ("worqai.io", "link en la bio", "registr", "prueba", "try", "reply", "comenta")):
        issues.append({"severity": "low", "penalty": 1, "problem": "The next action is unclear.", "fix": "Close with one proportionate action."})
    return issues


def _rewrite(task: MarketingTask, script: str) -> str:
    sentences = _sentences(script)
    if not sentences:
        return script
    repaired = []
    for sentence in sentences:
        updated = sentence
        for pattern, replacement in RISKY_REPLACEMENTS:
            updated = re.sub(pattern, replacement, updated, flags=re.IGNORECASE)
        repaired.append(updated.strip())
    hook = _recommended_hook(task, script)
    body = repaired[1:] if repaired and hook.lower() == repaired[0].lower() else repaired
    body = _dedupe(body)
    if any(word in script.lower() for word in ("worqai", "ats", " cv", "cv ")) and not any("invent" in sentence.lower() for sentence in body):
        body.append("No se trata de inventar experiencia. Se trata de presentar con claridad la experiencia real que responde a la vacante.")
    cta = _cta(task, script)
    if cta and not any(cta.lower() in sentence.lower() for sentence in body):
        body.append(cta)
    selected = [hook, *body]
    while len(" ".join(selected).split()) > 180 and len(selected) > 4:
        selected.pop(-2)
    return "\n\n".join(sentence.rstrip(".") + "." for sentence in selected if sentence)


def _recommended_hook(task: MarketingTask, script: str) -> str:
    lowered = script.lower()
    if "cv" in lowered and any(
        word in lowered
        for word in ("ats", "vacante", "puesto", "reclut", "descripcion", "descripción", "humano")
    ):
        return "Su CV puede estar ocultando la experiencia que esta vacante necesita encontrar"
    if "linkedin" in lowered or "perfil" in lowered:
        return "Su perfil puede tener experiencia valiosa y aun así no dar una razón clara para seguir leyendo"
    if "entrevista" in lowered or "interview" in lowered:
        return "Los nervios no significan que no esté preparado; significan que necesita una forma más simple de responder"
    first = _first_substantial_line(script)
    return first if len(first.split()) <= 18 else " ".join(first.split()[:18])


def _source_facts(script: str) -> list[str]:
    return [sentence for sentence in _sentences(script) if len(sentence.split()) >= 6][:6]


def _what_to_keep(script: str) -> list[str]:
    facts = _source_facts(script)
    return facts[:3] or ["Preserve the original subject and strongest factual claim."]


def _what_to_cut(script: str) -> list[str]:
    recommendations = ["Repeated context before the first useful consequence."]
    if len(script.split()) > 180:
        recommendations.append("Secondary explanations that do not change the viewer's next action.")
    if any(re.search(pattern, script.lower()) for pattern, _ in RISKY_REPLACEMENTS):
        recommendations.append("Absolute language that the available evidence cannot support.")
    return recommendations


def _visual_beats(task: MarketingTask, rewritten: str) -> list[str]:
    sentences = _sentences(rewritten)
    beats = [
        f"Hook on screen: {sentences[0][:90]}",
        f"Show the concrete problem behind {task.topic}.",
        "Reveal one source fact as text or product evidence.",
        "Show the mechanism or before/after instead of adding another explanation.",
        f"Final action: {_cta(task, rewritten)}",
    ]
    return beats


def _best_line(script: str) -> str:
    candidates = _sentences(script)
    if not candidates:
        return ""
    return max(candidates, key=lambda line: (any(word in line.lower() for word in ("no se trata", "sin invent", "evidencia", "vacante")), min(len(line), 160)))


def _cta(task: MarketingTask, script: str) -> str:
    lowered = script.lower()
    if "worqai" in lowered or "cv" in lowered:
        return "Pruebe WorqAI con una vacante real en worqai.io y revise la versión antes de enviarla"
    if task.channel.lower() == "linkedin":
        return "Revise el primer bloque de su perfil y pregunte si deja clara la evidencia principal"
    return "Pruebe este cambio con un ejemplo real y compare el resultado"


def _clean(script: str) -> str:
    return re.sub(r"[ \t]+", " ", script.strip())


def _sentences(script: str) -> list[str]:
    return [part.strip(" .") for part in re.split(r"(?<=[.!?])\s+|\n+", script) if len(part.split()) >= 3]


def _dedupe(sentences: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for sentence in sentences:
        key = re.sub(r"\W+", " ", sentence.lower()).strip()
        if key and key not in seen:
            output.append(sentence)
            seen.add(key)
    return output


def _first_substantial_line(script: str) -> str:
    for line in re.split(r"\n+|(?<=[.!?])\s+", script):
        line = line.strip()
        if len(line.split()) >= 5:
            return line
    return script.strip()[:160]


def _hook_has_tension(hook: str) -> bool:
    signals = ("descart", "humano", "leer", "perdido", "rechaz", "compet", "nerv", "problema", "nadie", "no ")
    return any(signal in hook.lower() for signal in signals)


def _duration(word_count: int) -> str:
    low = max(round(word_count / 3.0), 1)
    high = max(round(word_count / 2.4), low)
    return f"{low}-{high} seconds"


def _score_label(score: int) -> str:
    if score >= 9:
        return "production-ready after factual review"
    if score >= 7:
        return "strong but needs tightening"
    if score >= 5:
        return "usable draft"
    return "needs rewrite"


def _diagnosis(score: int, word_count: int, hook: str, topic: str) -> str:
    return f"The source contains a usable idea about {topic}. It scores {score}/10, runs about {word_count} words, and currently opens with: '{hook[:90]}'."
