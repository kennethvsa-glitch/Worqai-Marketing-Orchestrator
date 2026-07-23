"""Request-sensitive SEO planning grounded in search intent."""

from __future__ import annotations

import re

from .models import MarketingTask


KEYWORD_PAGES = {
    "cv con ia": ("/cv-con-ia", "CV con IA | Adapta tu CV a cada vacante", "Adapta tu CV con IA para cada puesto"),
    "analizador cv ats": ("/analizador-cv-ats", "Analizador de CV ATS | Revisa tu CV antes de aplicar", "Analiza la alineación de tu CV con una vacante"),
    "adaptar cv a vacante": ("/adaptar-cv-a-vacante", "Cómo adaptar tu CV a una vacante", "Convierte la vacante en la estrategia de tu CV"),
    "crear cv con ia": ("/crear-cv-con-ia", "Crear un CV con IA sin inventar experiencia", "Crea una versión de tu CV enfocada en el puesto"),
    "ai resume builder": ("/resume-builder-ai", "AI Resume Builder for Role-Specific Applications", "Build a resume around the role you want"),
}


def build_seo_plan(request: MarketingTask | str) -> dict[str, object]:
    task = _as_task(request)
    keyword = _primary_keyword(task.request)
    slug, title, h1 = KEYWORD_PAGES[keyword]
    market_suffix = "" if task.market == "LatAm" else f" en {task.market}"
    priority = _priority_pages(keyword)
    return {
        "format": "SEO implementation plan",
        "status": "requires_serp_validation",
        "primary_keyword": keyword,
        "market": task.market,
        "audience": task.audience,
        "search_intent": _intent(keyword),
        "primary_page": {
            "slug": slug,
            "keyword": keyword,
            "title": f"{title}{market_suffix}",
            "h1": f"{h1}{market_suffix}",
            "meta_description": _meta(keyword, task.market),
            "proof_required": "One real vacancy-to-CV before/after plus a visible product workflow.",
            "cta": "Analyze one CV against one real vacancy.",
        },
        "priority_pages": priority,
        "page_outline": _outline(keyword),
        "content_cluster": _content_cluster(keyword),
        "internal_link_map": _internal_links(slug),
        "schema": ["SoftwareApplication", "Organization", "BreadcrumbList", "FAQPage only when the visible FAQ is present"],
        "technical_checks": [
            "Implement in the cv-tailored Next.js workspace, not worqai-launch.",
            "Verify indexability, canonical URL, sitemap inclusion, status code, rendered title/H1, and mobile content.",
            "Link the page from a crawlable relevant hub and from supporting articles.",
            "Submit or inspect the URL in Google Search Console after deployment.",
        ],
        "research_requirements": [
            f"Inspect the current top results for '{keyword}' in the target market.",
            "Record competitor promises, page structures, proof, FAQs, and weak claims with source URLs.",
            "Validate demand and wording in Search Console or keyword data before scaling the cluster.",
        ],
        "measurement": ["indexed", "query impressions", "clicks", "CTR", "average position", "signup or CV-analysis conversion"],
        "source_request": task.request,
    }


def _as_task(value: MarketingTask | str) -> MarketingTask:
    if isinstance(value, MarketingTask):
        return value
    from .router import classify

    return classify(value)


def _primary_keyword(text: str) -> str:
    lowered = text.lower()
    aliases = (
        ("analizador", "analizador cv ats"), ("ats checker", "analizador cv ats"),
        ("adaptar", "adaptar cv a vacante"), ("tailor", "adaptar cv a vacante"),
        ("crear cv", "crear cv con ia"), ("resume builder", "ai resume builder"),
        ("cv con ia", "cv con ia"),
    )
    for signal, keyword in aliases:
        if signal in lowered:
            return keyword
    match = re.search(r"(?:rank for|posicionar|keyword|palabra clave)\s+['\"]?([^'\",.]+)", lowered)
    if match:
        candidate = match.group(1).strip()
        return min(KEYWORD_PAGES, key=lambda item: 0 if item in candidate or candidate in item else 1)
    return "cv con ia"


def _priority_pages(primary: str) -> list[dict[str, str]]:
    ordered = [primary, *[keyword for keyword in KEYWORD_PAGES if keyword != primary]]
    return [
        {"slug": KEYWORD_PAGES[keyword][0], "keyword": keyword, "title": KEYWORD_PAGES[keyword][1], "h1": KEYWORD_PAGES[keyword][2], "priority": "primary" if keyword == primary else "supporting"}
        for keyword in ordered
    ]


def _intent(keyword: str) -> str:
    if "analizador" in keyword:
        return "Evaluate an existing CV against ATS or vacancy criteria before applying."
    if "adaptar" in keyword:
        return "Tailor an existing CV to one specific vacancy without inventing experience."
    if "crear" in keyword or "builder" in keyword:
        return "Create or rebuild a CV with AI assistance and inspect the resulting document."
    return "Use a Spanish AI CV tool that can analyze and adapt an existing CV."


def _meta(keyword: str, market: str) -> str:
    location = " para Latinoamérica" if market == "LatAm" else f" en {market}"
    return f"Compara tu CV con una vacante y adapta tu experiencia real con WorqAI{location}. Empieza gratis."


def _outline(keyword: str) -> list[dict[str, str]]:
    return [
        {"section": "hero", "job": f"Confirm the {keyword} intent and let the visitor start the workflow."},
        {"section": "interactive proof", "job": "Show one vacancy requirement mapped to current and adapted CV evidence."},
        {"section": "how it works", "job": "Explain upload, compare, review gaps, adapt, and download."},
        {"section": "trust", "job": "State no-invention boundaries, review responsibility, and realistic ATS language."},
        {"section": "examples", "job": "Use role-specific before/after examples with sensitive data removed."},
        {"section": "faq", "job": "Answer actual SERP and user questions, then mirror only visible answers in schema."},
        {"section": "cta", "job": "Start one analysis with a real vacancy."},
    ]


def _content_cluster(primary: str) -> list[dict[str, str]]:
    topics = [
        ("/blog/que-es-un-ats", "Qué es un ATS y qué sí puede evaluar"),
        ("/blog/como-adaptar-cv-a-vacante", "Cómo adaptar un CV a una vacante sin inventar experiencia"),
        ("/blog/cv-generico-vs-adaptado", "CV genérico vs CV adaptado: ejemplo completo"),
        ("/blog/errores-cv-ats", "Errores de CV que ocultan evidencia relevante"),
    ]
    return [{"slug": slug, "title": title, "supports": primary} for slug, title in topics]


def _internal_links(primary_slug: str) -> list[dict[str, str]]:
    return [
        {"from": "/", "to": primary_slug, "anchor": "analizar y adaptar tu CV a una vacante"},
        {"from": "/blog/que-es-un-ats", "to": primary_slug, "anchor": "revisar la alineación de tu CV"},
        {"from": "/blog/como-adaptar-cv-a-vacante", "to": primary_slug, "anchor": "adaptar tu CV con WorqAI"},
    ]
