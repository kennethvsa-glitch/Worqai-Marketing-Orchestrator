"""Source-sensitive reframing for founder and community posts."""

from __future__ import annotations

import re


def reframe_social_post(request: str, original: str) -> dict[str, object]:
    cleaned = re.sub(r"[ \t]+", " ", original).strip()
    spanish = _is_spanish(f"{request} {cleaned}")
    audience = _audience(request)
    facts = _facts(cleaned)
    trust = _trust_notes(cleaned)
    recommended = _rewrite(cleaned, facts, audience, spanish=spanish, short=False)
    short = _rewrite(cleaned, facts, audience, spanish=spanish, short=True)
    return {
        "format": "social post reframe",
        "language": "es-LatAm" if spanish else "en",
        "audience": audience,
        "diagnosis": _diagnosis(cleaned, spanish=spanish),
        "source_facts": facts,
        "what_to_keep": _what_to_keep(cleaned, facts, spanish=spanish),
        "what_to_change": _what_to_change(cleaned, spanish=spanish),
        "recommended_post": recommended,
        "short_version": short,
        "comment_reply": _comment_reply(spanish=spanish),
        "hook_options": _hooks(facts, audience, spanish=spanish),
        "trust_notes": trust,
        "source_request": request,
        "original_word_count": len(cleaned.split()),
    }


def _rewrite(original: str, facts: list[str], audience: str, *, spanish: bool, short: bool) -> str:
    first_fact = facts[0] if facts else original[:180]
    product_fact = next((fact for fact in facts if "worq" in fact.lower() or "página" in fact.lower() or "tool" in fact.lower()), "")
    free = any(word in original.lower() for word in ("gratis", "free", "sin tarjeta", "no card"))
    local = any(word in original.lower() for word in ("tica", "costa rica", "latam", "latinoam"))
    if spanish:
        hook = _hooks(facts, audience, spanish=True)[0]
        mechanism = (
            "Usted sube su CV, pega una vacante real y WorqAI muestra qué evidencia está clara, "
            "qué falta hacer visible y cómo adaptar la redacción sin inventar experiencia."
        )
        proof = product_fact or first_fact
        if short:
            pieces = [hook, mechanism]
            if free:
                pieces.append("Puede empezar gratis y sin tarjeta.")
            pieces.append("Pruébelo en worqai.io y cuénteme qué parte le resultó útil o confusa.")
            return "\n\n".join(pieces)
        pieces = [
            hook,
            f"La razón para construirlo fue concreta: {first_fact.rstrip('.')}.",
            mechanism,
            f"Lo importante es esto: {proof.rstrip('.')}.",
        ]
        if free:
            pieces.append("Puede empezar gratis y sin tarjeta.")
        if local:
            pieces.append("Es un producto construido desde Costa Rica para personas que aplican en mercados competitivos de Latinoamérica.")
        pieces.append("Está en worqai.io. Si lo prueba, me interesa especialmente saber qué entendió rápido y qué todavía necesita mejorar.")
        return "\n\n".join(pieces)
    hook = _hooks(facts, audience, spanish=False)[0]
    mechanism = (
        "Upload the CV, paste a real vacancy, and WorqAI shows which evidence is clear, "
        "what is buried, and how to adapt the wording without inventing experience."
    )
    pieces = [hook, mechanism]
    if not short:
        pieces.insert(1, f"We built it because {first_fact.rstrip('.').lower()}.")
        pieces.append(f"The source idea worth keeping is: {product_fact or first_fact}")
    if free:
        pieces.append("You can start free without a card.")
    pieces.append("Try it at worqai.io and tell me what felt clear or confusing.")
    return "\n\n".join(pieces)


def _facts(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [sentence.strip() for sentence in sentences if len(sentence.split()) >= 5][:6]


def _audience(request: str) -> str:
    lowered = request.lower()
    if any(word in lowered for word in ("university", "universidad", "institution", "institución")):
        return "university and employability leaders"
    if any(word in lowered for word in ("company", "companies", "empresa", "b2b")):
        return "company and HR leaders"
    if any(word in lowered for word in ("latam", "latinoam")):
        return "LatAm job seekers"
    if any(word in lowered for word in ("costa rica", "tica", "brete")):
        return "job seekers in Costa Rica"
    return "job seekers and career communities"


def _hooks(facts: list[str], audience: str, *, spanish: bool) -> list[str]:
    fact = facts[0].rstrip(".") if facts else "aplicar a trabajos puede sentirse como enviar el CV al vacío"
    if spanish:
        return [
            f"Si {fact.lower()}, esto le puede servir.",
            "Hicimos una forma de revisar la alineación del CV antes de volver a enviarlo.",
            "Una vacante no debería obligarle a adivinar qué parte de su experiencia falta mostrar.",
        ]
    return [
        f"If {fact.lower()}, this may help.",
        "We built a way to check CV-to-role fit before sending another application.",
        "A vacancy should not make you guess which part of your experience is still invisible.",
    ]


def _diagnosis(text: str, *, spanish: bool) -> str:
    risks = []
    lowered = text.lower()
    if any(word in lowered for word in ("siempre", "todos", "garant", "never", "always")):
        risks.append("absolute claims")
    if len(text.split()) > 180:
        risks.append("excess length")
    if "ats" in lowered and "invent" not in lowered:
        risks.append("missing no-invention boundary")
    if spanish:
        return "La historia original tiene material útil y debe conservar sus hechos. La nueva versión ordena primero el problema, después el mecanismo y al final una sola invitación." + (f" Riesgos detectados: {', '.join(risks)}." if risks else "")
    return "The original contains useful facts that should be preserved. The rewrite orders the problem, mechanism, proof, and one invitation." + (f" Risks: {', '.join(risks)}." if risks else "")


def _what_to_keep(text: str, facts: list[str], *, spanish: bool) -> list[str]:
    items = facts[:3] or [text[:160]]
    prefix = "Hecho fuente: " if spanish else "Source fact: "
    return [prefix + item for item in items]


def _what_to_change(text: str, *, spanish: bool) -> list[str]:
    if spanish:
        return [
            "Mover el problema concreto al inicio.",
            "Explicar ATS como contexto, no como truco garantizado.",
            "Usar adaptar en lugar de generar cuando la experiencia ya existe.",
            "Cerrar con una sola acción y una invitación real a dar feedback.",
        ]
    return [
        "Move the concrete problem to the opening.",
        "Explain ATS as context, not a guaranteed hack.",
        "Use tailor or adapt when the source experience already exists.",
        "Close with one action and a genuine request for feedback.",
    ]


def _trust_notes(text: str) -> list[str]:
    notes = ["Preserve factual claims from the source; do not manufacture proof."]
    if "ats" in text.lower():
        notes.append("Use 'many systems' and 'can' rather than universal ATS claims.")
    if any(word in text.lower() for word in ("gratis", "free")):
        notes.append("Keep the free claim beside its current conditions, including card requirements.")
    return notes


def _comment_reply(*, spanish: bool) -> str:
    if spanish:
        return "Gracias por probarlo. La idea es adaptar experiencia real a una vacante específica, no inventarla ni prometer entrevistas. ¿Qué parte le resultó más útil?"
    return "Thanks for trying it. The goal is to adapt real experience to one role, not invent it or promise interviews. Which part was most useful?"


def _is_spanish(text: str) -> bool:
    return bool(re.search(r"[áéíóúñ¿¡]", text.lower())) or any(
        word in text.lower() for word in ("cv", "vacante", "trabajo", "brete", "gratis", "usted", "página")
    )
