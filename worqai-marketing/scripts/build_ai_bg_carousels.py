#!/usr/bin/env python3
"""
build_ai_bg_carousels.py — Generate 3 WorqAI 4-slide carousel variants
using the ai-bubbles-01 background with different visual systems.

Output:
    production/ai-bg-brand-s17.html
    production/ai-bg-premium-s01.html
    production/ai-bg-cyber-s29.html
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from render_carousel import render_carousel

# ═══ Shared background layer ═══
BG_LAYER = ["ai-bubbles-01"]

# ═══ Variant A: Brand (s17) — Lime, energetic, confident ═══
SPEC_BRAND = {
    "meta": {
        "system": "s17",
        "aspect": "1:1",
        "slides": 4,
        "brand": "@worqai",
        "language": "es-LATAM",
        "topic": "ai-bg-brand",
        "bg_recipe": "glow_bloom",   # energy builds toward CTA — bubbles get bioluminescent
    },
    "pacing": ["hook", "problem", "solution", "cta"],
    "slides": [
        {
            "id": "s1",
            "layout": "slide-hook-lockup",
            "layers": BG_LAYER,
            "copy": {
                "kicker": "WorqAI",
                "headline": "Tu CV nunca\nfue leído.",
                "body": "El ATS lo rechazó antes de que un humano lo viera.",
            },
        },
        {
            "id": "s2",
            "layout": "slide-big-number",
            "layers": BG_LAYER,
            "copy": {
                "kicker": "El problema",
                "stat_number": "75%",
                "stat_context": "de CVs rechazados",
                "headline": "El filtro automático gana.",
                "body": "Sin optimización ATS, tu experiencia no importa.",
            },
        },
        {
            "id": "s3",
            "layout": "slide-hook-lockup",
            "layers": BG_LAYER,
            "copy": {
                "kicker": "La solución",
                "headline": "WorqAI\nreescribe todo.",
                "body": "IA que optimiza tu CV para pasar cualquier ATS.",
            },
        },
        {
            "id": "s4",
            "layout": "slide-cta",
            "layers": BG_LAYER,
            "copy": {
                "question": "¿Listo para que te lean?",
                "cta_keyword": "OPTIMIZAR",
                "reward": "Primer rewrite gratis. Resultados en 48h.",
            },
        },
    ],
}

# ═══ Variant B: Premium (s01) — Gold, aspirational, luxury ═══
SPEC_PREMIUM = {
    "meta": {
        "system": "s01",
        "aspect": "1:1",
        "slides": 4,
        "brand": "@worqai",
        "language": "es-LATAM",
        "topic": "ai-bg-premium",
        "bg_recipe": "deep_zoom",    # dreamy blur → razor-sharp, cinematic arc
    },
    "pacing": ["hook", "problem", "solution", "cta"],
    "slides": [
        {
            "id": "s1",
            "layout": "slide-hook-lockup",
            "layers": BG_LAYER,
            "copy": {
                "kicker": "Premium",
                "headline": "El empleo\nque merecés.",
                "body": "Tu talento es real. Tu formato es el problema.",
            },
        },
        {
            "id": "s2",
            "layout": "slide-big-number",
            "layers": BG_LAYER,
            "copy": {
                "kicker": "La barrera",
                "stat_number": "6s",
                "stat_context": "de atención del ATS",
                "headline": "Decides en segundos.",
                "body": "Si el ATS no entiende tu estructura, pasas a la papelera.",
            },
        },
        {
            "id": "s3",
            "layout": "slide-proof",
            "layers": BG_LAYER,
            "copy": {
                "kicker": "Resultado",
                "headline": "De 0 a 4 entrevistas.",
                "quote": "Cambié el formato. No el contenido. Y empezaron a llamarme.",
                "attribution": "María L · Product Manager · 2026",
                "stat_number": "+4",
                "stat_context": "entrevistas en 14 días",
                "body": "Keywords correctas + estructura plana sin tablas.",
            },
        },
        {
            "id": "s4",
            "layout": "slide-cta",
            "layers": BG_LAYER,
            "copy": {
                "question": "¿Querés que tu CV brille?",
                "cta_keyword": "ELEVAR",
                "reward": "CV premium. Entrega en 48 horas.",
            },
        },
    ],
}

# ═══ Variant C: Cyberpunk (s29) — Neon, tech, hacker ethos ═══
SPEC_CYBER = {
    "meta": {
        "system": "s29",
        "aspect": "1:1",
        "slides": 4,
        "brand": "@worqai",
        "language": "es-LATAM",
        "topic": "ai-bg-cyber",
        "bg_recipe": "phase_distort",  # glass warp deepens — techy, unsettling refraction
    },
    "pacing": ["hook", "problem", "solution", "cta"],
    "slides": [
        {
            "id": "s1",
            "layout": "slide-terminal",
            "layers": BG_LAYER,
            "copy": {
                "kicker": "SYSTEM BREACH",
                "headline": "Tu CV fue\nignorado.",
                "output_lines": [
                    {"type": "err", "text": "ATS_REJECTION: CV no parseable"},
                    {"type": "warn", "text": "FORMAT_ERROR: tablas detectadas"},
                    {"type": "info", "text": "KEYWORD_MATCH: 3/20 (CRITICO)"},
                    {"type": "ok", "text": "WORQAI_OVERRIDE: ready"},
                ],
            },
        },
        {
            "id": "s2",
            "layout": "slide-big-number",
            "layers": BG_LAYER,
            "copy": {
                "kicker": "FIREWALL STATS",
                "stat_number": "75%",
                "stat_context": "bloqueados",
                "headline": "El ATS es el gatekeeper.",
                "body": "No es el reclutador. Es el algoritmo.",
            },
        },
        {
            "id": "s3",
            "layout": "slide-hook-lockup",
            "layers": BG_LAYER,
            "copy": {
                "kicker": "EXPLOIT DEPLOYED",
                "headline": "Bypass\ngarantizado.",
                "body": "WorqAI inyecta tu CV directo al recruiter. Sin filtros.",
            },
        },
        {
            "id": "s4",
            "layout": "slide-cta",
            "layers": BG_LAYER,
            "copy": {
                "question": "¿Inyectamos tu CV?",
                "cta_keyword": "HACKEAR",
                "reward": "Bypass ATS activado. Resultados inmediatos.",
            },
        },
    ],
}


def main():
    PROD = ROOT / "production"
    PROD.mkdir(parents=True, exist_ok=True)

    variants = [
        ("ai-bg-brand-s17.html", SPEC_BRAND),
        ("ai-bg-premium-s01.html", SPEC_PREMIUM),
        ("ai-bg-cyber-s29.html", SPEC_CYBER),
    ]

    for filename, spec in variants:
        out_path = PROD / filename
        print(f"\n-> Rendering {filename}")
        render_carousel(spec, out_path)
        size_kb = out_path.stat().st_size // 1024
        print(f"   [OK] {out_path} ({size_kb} KB)")

    print("\n[DONE] All 3 variants rendered in production/")


if __name__ == "__main__":
    main()
