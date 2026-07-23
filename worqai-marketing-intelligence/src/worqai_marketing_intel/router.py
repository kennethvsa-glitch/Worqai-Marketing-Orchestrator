"""Classify English and Spanish requests into compact marketing tasks."""

from __future__ import annotations

from dataclasses import replace
import re
import unicodedata

from .context_compiler import enrich_task
from .models import AssetType, MarketingTask


# Scores reflect specificity. Generic channel/topic words stay below explicit
# asset phrases so a supporting intent cannot take over the requested output.
ROUTE_SIGNALS: dict[AssetType, dict[str, int]] = {
    AssetType.MESSAGE_REPLY: {
        "message reply": 14,
        "comment reply": 14,
        "dm reply": 14,
        "reply": 7,
        "respond": 7,
        "respuesta": 7,
        "responder": 7,
        "contestar": 7,
    },
    AssetType.CAMPAIGN_PACKAGE: {
        "campaign package": 18,
        "launch package": 18,
        "full campaign": 15,
        "multi channel campaign": 15,
        "paquete de campana": 18,
        "campana completa": 15,
    },
    AssetType.SEO_PAGE: {
        "seo plan": 18,
        "plan seo": 18,
        "seo campaign": 16,
        "campana seo": 16,
        "search engine optimization": 16,
        "rank on google": 14,
        "rank in google": 14,
        "posicionar en google": 14,
        "posicionamiento seo": 16,
        "seo": 10,
        "serp": 8,
        "ranking": 6,
    },
    AssetType.DEEP_RESEARCH: {
        "deep research": 18,
        "competitor analysis": 16,
        "benchmark study": 15,
        "investigacion profunda": 18,
        "analisis de competencia": 16,
        "analisis de competidores": 16,
    },
    AssetType.FEEDBACK_LOOP: {
        "feedback loop": 18,
        "learn from performance": 15,
        "ciclo de retroalimentacion": 18,
        "search console": 10,
        "impressions": 6,
        "impresiones": 6,
        "ctr": 6,
    },
    AssetType.IG_REEL: {
        "instagram reel": 16,
        "ig reel": 16,
        "reel script": 15,
        "guion para reel": 16,
        "guion de reel": 16,
        "reel": 11,
        "reels": 11,
        "guion": 10,
        "tiktok": 8,
        "shorts": 8,
    },
    AssetType.CAROUSEL: {
        "linkedin carousel": 16,
        "slide deck": 13,
        "carousel": 12,
        "carrusel": 12,
        "slides": 8,
        "diapositivas": 8,
    },
    AssetType.MOTION_HANDOFF: {
        "motion studio handoff": 20,
        "motion handoff": 18,
        "render manifest": 16,
        "scene manifest": 15,
        "entrega a motion studio": 18,
    },
    AssetType.MOTION_VIDEO: {
        "motion video": 16,
        "video animado": 14,
        "storyboard": 12,
        "motion": 10,
        "animation": 10,
        "animacion": 10,
        "video": 8,
        "escena": 6,
    },
    AssetType.PARTNERSHIP_PITCH: {
        "partnership pitch": 18,
        "company pitch": 16,
        "propuesta comercial": 17,
        "propuesta de alianza": 18,
        "pitch": 12,
        "proposal": 12,
        "propuesta": 12,
        "partnership": 10,
        "alianza": 10,
        "outreach": 8,
        "university": 4,
        "universities": 4,
        "universidad": 4,
        "universidades": 4,
        "institution": 4,
        "institucion": 4,
        "campus": 4,
    },
    AssetType.LANDING_PAGE: {
        "landing page": 16,
        "pagina de aterrizaje": 16,
        "homepage": 12,
        "pagina web": 10,
        "landing": 10,
        "website": 8,
        "pricing page": 10,
    },
    AssetType.LINKEDIN_POST: {
        "linkedin post": 16,
        "post de linkedin": 16,
        "linkedin": 8,
        "thread": 8,
        "hilo": 8,
        "post": 7,
    },
    AssetType.AD: {
        "paid ad": 15,
        "ad creative": 15,
        "creative angle": 12,
        "anuncio pagado": 15,
        "anuncio": 12,
        "publicidad": 10,
        "ads": 11,
        "ad": 11,
    },
    AssetType.EMAIL: {
        "email sequence": 16,
        "secuencia de correos": 16,
        "newsletter": 12,
        "email": 11,
        "correo": 11,
        "correos": 11,
    },
    AssetType.CONTENT_SYSTEM: {
        "content system": 16,
        "content engine": 15,
        "sistema de contenido": 16,
        "content calendar": 14,
        "calendario de contenido": 14,
    },
    AssetType.BRAND: {
        "brand strategy": 15,
        "estrategia de marca": 15,
        "positioning": 11,
        "posicionamiento": 11,
        "brand": 9,
        "marca": 9,
    },
    AssetType.RESEARCH: {
        "successful examples": 10,
        "benchmark examples": 10,
        "ejemplos exitosos": 10,
        "casos exitosos": 9,
        "research": 9,
        "benchmark": 8,
        "benchmarks": 8,
        "competitor": 7,
        "competitors": 7,
        "investiga": 9,
        "investigar": 9,
        "investigacion": 9,
        "referencias": 7,
        "competencia": 7,
        "ejemplos": 6,
    },
    AssetType.CAMPAIGN: {
        "go to market": 14,
        "marketing campaign": 13,
        "campana de marketing": 13,
        "campaign": 11,
        "campana": 11,
        "gtm": 10,
        "launch": 8,
        "lanzamiento": 8,
    },
}

SUPPORTING_ASSETS = {AssetType.RESEARCH, AssetType.DEEP_RESEARCH}
CREATION_WORDS = {
    "build", "create", "draft", "generate", "make", "prepare", "write",
    "arma", "crear", "crea", "escribe", "genera", "haz", "prepara", "redacta",
}
RESEARCH_COMMANDS = {
    "benchmark", "investiga", "investigar", "investigate", "research", "study",
}
SPANISH_WORDS = {
    "alianza", "anuncio", "campana", "carrusel", "correo", "crea", "crear",
    "ejemplos", "empresa", "guion", "haz", "investiga", "mensaje", "para",
    "propuesta", "publicidad", "respuesta", "universidad", "video",
}

# Stable tie-breaking favors the more specific production format.
ASSET_PRECEDENCE = tuple(ROUTE_SIGNALS)


def classify(request: str) -> MarketingTask:
    normalized = normalize_text(request)
    tokens = normalized.split()
    scores: dict[AssetType, int] = {}
    matches: dict[AssetType, list[str]] = {}
    explicit_assets: set[AssetType] = set()

    for asset_type, signals in ROUTE_SIGNALS.items():
        asset_matches = [phrase for phrase in signals if has_phrase(normalized, phrase)]
        if not asset_matches:
            continue
        matches[asset_type] = asset_matches
        scores[asset_type] = sum(signals[phrase] for phrase in asset_matches)
        if asset_type not in SUPPORTING_ASSETS and _explicit_creation(normalized, asset_matches):
            scores[asset_type] += 20
            explicit_assets.add(asset_type)

    if tokens and tokens[0] in RESEARCH_COMMANDS:
        research_type = AssetType.DEEP_RESEARCH if AssetType.DEEP_RESEARCH in scores else AssetType.RESEARCH
        scores[research_type] = scores.get(research_type, 0) + 8

    selected = _select_asset(scores, explicit_assets)
    referenced_asset = _strongest_primary(scores)
    selected_matches = matches.get(selected, [])
    task = MarketingTask(
        request=request,
        asset_type=selected,
        topic=_topic(request),
        audience=_audience(normalized),
        signals=tuple(selected_matches),
    )
    task = enrich_task(task)

    language = "es-LatAm" if set(tokens) & SPANISH_WORDS else task.language
    metadata = dict(task.metadata)
    metadata.update(
        {
            "routing_scores": {
                asset_type.value: score
                for asset_type, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)
            },
            "explicit_primary_asset": selected in explicit_assets,
            "referenced_asset_type": (
                referenced_asset.value
                if selected in SUPPORTING_ASSETS and referenced_asset is not None
                else ""
            ),
        }
    )
    return replace(task, language=language, metadata=metadata)


def normalize_text(text: str) -> str:
    """Return lowercase ASCII tokens while preserving phrase boundaries."""

    decomposed = unicodedata.normalize("NFKD", text.casefold())
    without_marks = "".join(char for char in decomposed if not unicodedata.combining(char))
    return " ".join(re.findall(r"[a-z0-9]+", without_marks))


def has_phrase(text: str, phrase: str) -> bool:
    """Match a normalized token or phrase, never a substring of another word."""

    normalized_text = normalize_text(text)
    normalized_phrase = normalize_text(phrase)
    if not normalized_phrase:
        return False
    return re.search(rf"(?:^| )\b{re.escape(normalized_phrase)}\b(?: |$)", normalized_text) is not None


def _explicit_creation(text: str, matched_phrases: list[str]) -> bool:
    command = "(?:" + "|".join(sorted(CREATION_WORDS)) + ")"
    articles = r"(?:(?:a|an|the|el|la|los|las|un|una) )?"
    modifiers = r"(?:(?:complete|completa|completo|full|new|nueva|nuevo|short|social) ){0,2}"
    for phrase in matched_phrases:
        normalized_phrase = normalize_text(phrase)
        pattern = rf"(?:^| )\b{command}\b {articles}{modifiers}\b{re.escape(normalized_phrase)}\b"
        if re.search(pattern, text):
            return True
    return False


def _select_asset(scores: dict[AssetType, int], explicit_assets: set[AssetType]) -> AssetType:
    if explicit_assets:
        candidates = explicit_assets
    elif scores:
        candidates = set(scores)
    else:
        return AssetType.CAMPAIGN
    precedence = {asset_type: index for index, asset_type in enumerate(ASSET_PRECEDENCE)}
    return max(candidates, key=lambda asset_type: (scores[asset_type], -precedence[asset_type]))


def _strongest_primary(scores: dict[AssetType, int]) -> AssetType | None:
    primary_scores = {
        asset_type: score for asset_type, score in scores.items() if asset_type not in SUPPORTING_ASSETS
    }
    if not primary_scores:
        return None
    precedence = {asset_type: index for index, asset_type in enumerate(ASSET_PRECEDENCE)}
    return max(primary_scores, key=lambda asset_type: (primary_scores[asset_type], -precedence[asset_type]))


def _audience(text: str) -> str:
    if any(has_phrase(text, phrase) for phrase in (
        "university", "universities", "universidad", "universidades", "campus", "school",
        "institution", "institucion",
    )):
        return "career centers, universities, institutions, and workforce programs"
    if any(has_phrase(text, phrase) for phrase in (
        "company", "companies", "empresa", "empresas", "employer", "b2b", "business",
    )):
        return "companies, HR teams, workforce leaders, and business operators"
    if any(has_phrase(text, phrase) for phrase in (
        "recruiter", "reclutador", "coach", "agency", "agencia",
    )):
        return "recruiters, coaches, and career service operators"
    if any(has_phrase(text, phrase) for phrase in (
        "candidate", "candidato", "job seeker", "job seekers", "resume", "cv", "ats", "latam",
    )):
        return "job seekers applying to competitive roles"
    return "job seekers and career operators"


def _topic(request: str) -> str:
    cleaned = re.sub(r"\s+", " ", request).strip()
    return cleaned[:120]
