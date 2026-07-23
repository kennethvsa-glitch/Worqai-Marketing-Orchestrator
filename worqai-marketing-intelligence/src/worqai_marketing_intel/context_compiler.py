"""Compile loose prompts into compact, reusable marketing context."""

from __future__ import annotations

import re
from dataclasses import replace

from .models import AssetType, MarketingTask


SPANISH_SIGNALS = {
    "adaptar", "aplicar", "buscando", "carrusel", "comentario", "correo",
    "crea", "cv", "empleo", "empresa", "guion", "haz", "mensaje", "puesto",
    "respuesta", "universidad", "vacante", "video",
}

COUNTRIES = {
    "costa rica": "Costa Rica",
    "mexico": "Mexico",
    "méxico": "Mexico",
    "colombia": "Colombia",
    "peru": "Peru",
    "perú": "Peru",
    "panama": "Panama",
    "panamá": "Panama",
    "argentina": "Argentina",
    "chile": "Chile",
    "latam": "LatAm",
    "latinoamerica": "LatAm",
    "latinoamérica": "LatAm",
}


def enrich_task(task: MarketingTask) -> MarketingTask:
    request, source_text = split_source_text(task.request)
    lowered = request.lower()
    language = detect_language(task.request)
    market = detect_market(lowered)
    audience = detect_audience(lowered, task.audience)
    topic = extract_topic(request, task.asset_type)
    objective = detect_objective(lowered, task.asset_type)
    channel = detect_channel(lowered, task.asset_type)
    offer = detect_offer(lowered)
    constraints = extract_constraints(lowered)
    research_requested = any(
        phrase in lowered
        for phrase in (
            "research", "benchmark", "successful examples", "competitor",
            "investiga", "ejemplos exitosos", "referencias", "competencia",
        )
    )
    metadata: dict[str, object] = {
        "requested_count": extract_requested_count(lowered),
        "address": "usted" if any(word in lowered for word in ("usted", "ustedes")) else "tu",
        "organization": extract_organization(request),
        "source_facts": source_facts(source_text),
    }
    return replace(
        task,
        request=request,
        topic=topic,
        audience=audience,
        language=language,
        market=market,
        objective=objective,
        channel=channel,
        offer=offer,
        source_text=source_text,
        constraints=constraints,
        research_requested=research_requested,
        metadata=metadata,
    )


def split_source_text(prompt: str) -> tuple[str, str]:
    lowered = prompt.lower()
    markers = (
        "script:", "guion:", "guión:", "post:", "copy:", "texto:",
        "message:", "mensaje:", "comment:", "comentario:", "dm:",
    )
    for marker in markers:
        index = lowered.find(marker)
        if index >= 0:
            request = prompt[:index].strip(" :-")
            source = prompt[index + len(marker):].strip()
            if source:
                return request or prompt, source
    if "|" in prompt:
        request, source = (part.strip() for part in prompt.split("|", maxsplit=1))
        if request and source:
            return request, source
    return prompt.strip(), ""


def detect_language(text: str) -> str:
    lowered = text.lower()
    words = set(re.findall(r"[a-záéíóúüñ]+", lowered))
    spanish_hits = len(words & SPANISH_SIGNALS)
    spanish_commands = {"crea", "crear", "haz", "dame", "escribe", "redacta", "audita", "mejora", "revisa"}
    if words & spanish_commands or spanish_hits >= 2 or re.search(r"[áéíóúüñ¿¡]", lowered):
        return "es-LatAm"
    return "en"


def detect_market(text: str) -> str:
    for signal, market in COUNTRIES.items():
        if signal in text:
            return market
    return "LatAm"


def detect_audience(text: str, fallback: str) -> str:
    if any(word in text for word in ("universidad", "universidades", "university", "campus", "career center")):
        return "university career centers and employability leaders"
    if any(word in text for word in ("empresa", "empresas", "company", "companies", "hr team", "recursos humanos")):
        return "companies, HR teams, and workforce leaders"
    if any(word in text for word in ("recruiter", "reclutador", "coach", "agencia", "agency")):
        return "recruiters, career coaches, and service operators"
    if any(word in text for word in ("graduado", "graduados", "graduate", "student", "estudiante", "primer empleo")):
        return "students and early-career job seekers"
    if any(word in text for word in ("ejecutivo", "executive", "senior", "manager", "gerente")):
        return "experienced professionals applying to senior roles"
    if any(word in text for word in ("job seeker", "buscando trabajo", "buscando brete", "candidato", "candidate", "cv", "resume")):
        return "LatAm job seekers applying to competitive roles"
    return fallback


def detect_objective(text: str, asset_type: AssetType) -> str:
    if any(word in text for word in ("signup", "registro", "convert", "conversion", "descarga", "download")):
        return "conversion"
    if any(word in text for word in ("pitch", "propuesta", "pilot", "piloto", "meeting", "reunion", "reunión")):
        return "partnership lead generation"
    if any(word in text for word in ("educate", "explain", "enseñar", "explicar", "mitos", "myths")):
        return "education and trust"
    if any(word in text for word in ("launch", "lanzamiento", "awareness", "conocimiento")):
        return "launch awareness"
    if asset_type == AssetType.PARTNERSHIP_PITCH:
        return "partnership lead generation"
    if asset_type in {AssetType.SEO_PAGE, AssetType.LANDING_PAGE}:
        return "organic acquisition"
    if asset_type == AssetType.MESSAGE_REPLY:
        return "trust and response"
    return "awareness and qualified product interest"


def detect_channel(text: str, asset_type: AssetType) -> str:
    channels = (
        ("linkedin", "LinkedIn"), ("instagram", "Instagram"),
        ("tiktok", "TikTok"), ("youtube", "YouTube"),
        ("whatsapp", "WhatsApp"), ("email", "Email"), ("correo", "Email"),
    )
    for signal, channel in channels:
        if signal in text:
            return channel
    defaults = {
        AssetType.IG_REEL: "Instagram Reels",
        AssetType.CAROUSEL: "LinkedIn and Instagram",
        AssetType.LINKEDIN_POST: "LinkedIn",
        AssetType.EMAIL: "Email",
        AssetType.SEO_PAGE: "Google Search",
        AssetType.MESSAGE_REPLY: "Direct message or comment",
        AssetType.MOTION_VIDEO: "Social video",
    }
    return defaults.get(asset_type, "multi-channel")


def detect_offer(text: str) -> str:
    if any(word in text for word in ("pilot", "piloto", "universidad", "university", "institucion", "institution")):
        return "a low-risk WorqAI pilot using real roles and before/after evidence"
    if any(word in text for word in ("free", "gratis", "sin tarjeta", "no card")):
        return "a free WorqAI CV analysis or first tailored CV without a card"
    if any(word in text for word in ("ats", "analizador", "score", "puntuar", "audit")):
        return "WorqAI CV-to-job fit analysis"
    return "WorqAI role-specific CV analysis and adaptation without inventing experience"


def extract_topic(request: str, asset_type: AssetType) -> str:
    normalized = re.sub(r"\s+", " ", request).strip()
    match = re.search(r"(?:about|sobre|para|for)\s+(.+)$", normalized, flags=re.IGNORECASE)
    topic = match.group(1).strip(" .") if match else normalized
    command_words = (
        "create", "make", "write", "draft", "give me", "audit", "rewrite",
        "crea", "crear", "haz", "escribe", "redacta", "dame", "audita", "mejora",
    )
    for command in command_words:
        topic = re.sub(rf"^{re.escape(command)}\s+", "", topic, flags=re.IGNORECASE)
    asset_words = {
        AssetType.CAROUSEL: ("a carousel", "carousel", "un carrusel", "carrusel"),
        AssetType.IG_REEL: ("ig reel", "reel", "reels", "guion", "guión"),
        AssetType.MOTION_VIDEO: ("motion video", "video", "animacion", "animación"),
        AssetType.PARTNERSHIP_PITCH: ("pitch", "proposal", "propuesta"),
    }
    for phrase in asset_words.get(asset_type, ()):
        topic = re.sub(rf"^{re.escape(phrase)}\s+", "", topic, flags=re.IGNORECASE)
    return (topic[:160].strip(" :-") or "role-specific CV applications")


def extract_constraints(text: str) -> tuple[str, ...]:
    constraints: list[str] = []
    duration = re.search(r"(?:under|menos de|max(?:imo)?|máximo)\s+(\d+)\s*(?:seconds|segundos|s)\b", text)
    if duration:
        constraints.append(f"maximum {duration.group(1)} seconds")
    slides = re.search(r"(\d+)\s*(?:slides|diapositivas)", text)
    if slides:
        constraints.append(f"exactly {slides.group(1)} slides")
    if any(word in text for word in ("formal", "professional", "profesional")):
        constraints.append("professional and restrained tone")
    if any(word in text for word in ("casual", "friendly", "amigable", "pura vida")):
        constraints.append("conversational and locally natural tone")
    if any(word in text for word in ("sin inventar", "without inventing", "no invent")):
        constraints.append("do not invent experience or proof")
    return tuple(dict.fromkeys(constraints))


def extract_requested_count(text: str) -> int:
    match = re.search(
        r"\b([1-9]|10)(?:\s+[a-záéíóúñ]+){0,3}\s+(?:ideas|concepts|angles|opciones|hooks|ganchos)\b",
        text,
    )
    return int(match.group(1)) if match else 3


def extract_organization(request: str) -> str:
    patterns = (
        r"(?:to|for|para|a)\s+([A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ&.-]+(?:\s+[A-ZÁÉÍÓÚÑ][\wÁÉÍÓÚÑáéíóúñ&.-]+){0,4})",
        r"(?:university|universidad|company|empresa|institution|institución)\s+([\wÁÉÍÓÚÑáéíóúñ&.-]+(?:\s+[\wÁÉÍÓÚÑáéíóúñ&.-]+){0,3})",
    )
    for pattern in patterns:
        match = re.search(pattern, request)
        if match:
            candidate = match.group(1).strip(" .")
            if candidate.lower() not in {"worqai", "latam", "job seekers", "universities"}:
                return candidate
    return ""


def source_facts(source_text: str, limit: int = 6) -> tuple[str, ...]:
    if not source_text:
        return ()
    sentences = re.split(r"(?<=[.!?])\s+|\n+", source_text)
    facts = [sentence.strip() for sentence in sentences if len(sentence.split()) >= 4]
    return tuple(facts[:limit])
