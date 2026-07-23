#!/usr/bin/env python3
"""Generate 10 WorqAI carousel specs using the new AI panel backgrounds."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
PRODUCTION = ROOT / "production"
PRODUCTION.mkdir(exist_ok=True)

# Each carousel: bg ID, primary system, topic slug, pacing, 4 slides
# Layer rules:
#   - 1 shared layer across all slides (in first position)
#   - Each slide gets a unique second layer
#   - glow-orb max 2× per carousel
#   - At least 1 demonstration layout per carousel

SPECS = [
    # ── 1. glowing-energy-flow + s04 ────────────────────────────────────────
    {
        "bg": "glowing-energy-flow",
        "system": "s04",
        "topic": "ats-no-lee-como-humano",
        "pacing": ["hook", "diagnostic", "solution", "cta"],
        "shared_layer": "geo-circuit-trace",
        "slides": [
            {
                "id": "s1",
                "layout": "slide-hook-lockup",
                "layers": ["geo-circuit-trace", "geo-mesh-noise"],
                "decoratives": [{"id": "svg-starburst-spark", "position": "tr"}],
                "copy": {
                    "kicker": "EL FILTRO INVISIBLE",
                    "headline": "Tu CV se ve bien. El ATS no opina igual.",
                    "body": "El 75% de las empresas usan un bot antes de que un humano vea tu hoja de vida. Diseño no es compatibilidad.",
                    "swipe_prompt": "Desliza →"
                },
                "custom_css": ".s1-display { font-size: clamp(32px,6.5cqw,48px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; } .s1-body { opacity: 0.85; font-size: 15px; max-width: 42ch; }"
            },
            {
                "id": "s2",
                "layout": "slide-terminal",
                "layers": ["geo-circuit-trace", "scan-lines"],
                "copy": {
                    "kicker": "DIAGNÓSTICO",
                    "headline": "Esto ve el bot cuando abre tu CV",
                    "command": "worqai --scan cv.pdf",
                    "tab_title": "worqai-scan",
                    "output_lines": [
                        {"type": "ok", "text": "Nombre detectado: OK"},
                        {"type": "warn", "text": "Tablas encontradas: 4 (el ATS las ignora)"},
                        {"type": "err", "text": "ERROR: Fechas sin formato estandar ISO"},
                        {"type": "info", "text": "Score de parseo: 34/100 — rechazado automatico"}
                    ]
                },
                "custom_css": ".s2-headline { font-size: clamp(22px,4.5cqw,32px); font-weight: 800; letter-spacing: -0.02em; }"
            },
            {
                "id": "s3",
                "layout": "slide-input-output",
                "layers": ["geo-circuit-trace", "glow-orb"],
                "decoratives": [{"id": "svg-starburst-burst", "position": "bl"}],
                "copy": {
                    "kicker": "EL PROBLEMA",
                    "headline": "Lo que envias vs. lo que lee el ATS",
                    "input_label": "Tu CV (se ve asi)",
                    "input_text": "Diseño visual con iconos, tablas de habilidades y graficos de progreso.",
                    "output_label": "El ATS lo lee asi",
                    "output_text": "[NOMBRE] [TEXTO SIN FORMATO] [DATOS PERDIDOS] Score: 28/100"
                },
                "custom_css": ".s3-headline { font-size: clamp(22px,4.5cqw,32px); font-weight: 800; letter-spacing: -0.02em; } .s3-panel-label { font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; opacity: 0.85; }"
            },
            {
                "id": "s4",
                "layout": "slide-cta",
                "layers": ["geo-circuit-trace", "geo-mesh-noise"],
                "decoratives": [{"id": "sub-stamp-circle", "text": "GRATIS"}],
                "copy": {
                    "question": "Tu CV sobrevive al bot o lo tira sin leer?",
                    "cta_keyword": "DIAGNOSTICO",
                    "reward": "Te decimos en 60 segundos que arreglar. Sin costo."
                },
                "custom_css": ".s4-question { font-size: clamp(26px,5.5cqw,38px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; } .s4-reward { opacity: 0.85; }"
            }
        ]
    },
    # ── 2. oceanic-wave + s17 ───────────────────────────────────────────────
    {
        "bg": "oceanic-wave",
        "system": "s17",
        "topic": "73-porciento-muere-filtro",
        "pacing": ["hook", "data", "solution", "cta"],
        "shared_layer": "geo-flow-wave",
        "slides": [
            {
                "id": "s1",
                "layout": "slide-big-number",
                "layers": ["geo-flow-wave", "pw-grid"],
                "decoratives": [{"id": "svg-starburst-spark", "position": "tr"}],
                "copy": {
                    "kicker": "DATO DURO",
                    "stat_number": "73%",
                    "stat_context": "Nunca los ve un humano. El bot decide.",
                    "headline": "La puerta esta cerrada para la mayoria"
                },
                "custom_css": ".s1-stat { font-size: clamp(72px,14cqw,110px); font-weight: 900; letter-spacing: -0.04em; } .s1-context { opacity: 0.85; max-width: 36ch; }"
            },
            {
                "id": "s2",
                "layout": "slide-input-output",
                "layers": ["geo-flow-wave", "geo-pixel-grid"],
                "copy": {
                    "kicker": "EL PROBLEMA",
                    "headline": "Lo que envias vs. lo que lee el ATS",
                    "input_label": "Tu CV (se ve asi)",
                    "input_text": "Diseño visual con iconos, tablas de habilidades y graficos de progreso.",
                    "output_label": "El ATS lo lee asi",
                    "output_text": "[NOMBRE] [TEXTO SIN FORMATO] [DATOS PERDIDOS] Score: 28/100"
                },
                "custom_css": ".s2-headline { font-size: clamp(22px,4.5cqw,32px); font-weight: 800; letter-spacing: -0.02em; } .s2-panel-label { font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; opacity: 0.85; }"
            },
            {
                "id": "s3",
                "layout": "slide-checklist",
                "layers": ["geo-flow-wave", "glow-orb"],
                "decoratives": [{"id": "svg-starburst-burst", "position": "bl"}],
                "copy": {
                    "kicker": "SOLUCION",
                    "headline": "3 reglas para entrar al 27%",
                    "items": [
                        "Texto plano, sin columnas ni tablas",
                        "Palabras clave del puesto copiadas tal cual",
                        "Formato .docx simple, no PDF con diseno"
                    ]
                },
                "custom_css": ".s3-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; } .s3-chk-title { font-size: 15px; font-weight: 600; }"
            },
            {
                "id": "s4",
                "layout": "slide-cta",
                "layers": ["geo-flow-wave", "geo-pixel-grid"],
                "decoratives": [{"id": "sub-stamp-circle", "text": "GRATIS"}],
                "copy": {
                    "question": "En que 27% queres estar?",
                    "cta_keyword": "REVISAR",
                    "reward": "Subi tu CV. Te decimos si el bot lo lee o lo ignora."
                },
                "custom_css": ".s4-question { font-size: clamp(26px,5.5cqw,38px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; }"
            }
        ]
    },
    # ── 3. pastel-waves + s25 ───────────────────────────────────────────────
    {
        "bg": "pastel-waves",
        "system": "s25",
        "topic": "errores-6-segundos",
        "pacing": ["hook", "diagnostic", "solution", "cta"],
        "shared_layer": "grid-bg",
        "slides": [
            {
                "id": "s1",
                "layout": "slide-contrast-knockout",
                "layers": ["grid-bg", "geo-data-streaks"],
                "copy": {
                    "kicker": "6 SEGUNDOS",
                    "headline": "Eso tarda un reclutador en tirar tu CV.",
                    "body": "No es crueldad. Es volumen: 250+ postulaciones por puesto."
                },
                "custom_css": ".s1-display { font-size: clamp(30px,6.5cqw,48px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; } .s1-body { opacity: 0.85; max-width: 38ch; }"
            },
            {
                "id": "s2",
                "layout": "slide-terminal-fullscreen",
                "layers": ["grid-bg", "scan-lines"],
                "copy": {
                    "headline": "El bot decidio en 0.4 segundos",
                    "code_lines": [
                        {"text": "[PASS] Nombre: OK", "type": "ok"},
                        {"text": "[FAIL] Tabla detectada: habilidades_blandas", "type": "err"},
                        {"text": "[FAIL] Fecha: 'hace 2 anos' → no parseable", "type": "err"},
                        {"text": "[FAIL] Email en imagen: no extraido", "type": "err"},
                        {"text": "RESULT: REJECTED — contacto no recuperable", "type": "info"}
                    ]
                },
                "custom_css": ".s2-headline { font-size: clamp(22px,4.5cqw,32px); font-weight: 800; letter-spacing: -0.02em; margin-bottom: 24px; }"
            },
            {
                "id": "s3",
                "layout": "slide-before-after",
                "layers": ["grid-bg", "glow-orb"],
                "decoratives": [{"id": "svg-starburst-burst", "position": "bl"}],
                "copy": {
                    "kicker": "ANTES / DESPUES",
                    "headline": "Mismo perfil, distinto resultado",
                    "before_items": ["PDF con columnas", "Titulos creativos", "Sin palabras clave"],
                    "after_items": [".docx lineal", "Titulos del puesto", "Verbos del aviso copiados"],
                    "before_score": "12",
                    "after_score": "89"
                },
                "custom_css": ".s3-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; } .s3-score { font-weight: 900; font-size: clamp(48px,10cqw,80px); letter-spacing: -0.04em; }"
            },
            {
                "id": "s4",
                "layout": "slide-cta",
                "layers": ["grid-bg", "geo-data-streaks"],
                "decoratives": [{"id": "sub-stamp-circle", "text": "GRATIS"}],
                "copy": {
                    "question": "Cuantos errores tiene tu CV?",
                    "cta_keyword": "AUDITAR",
                    "reward": "Escaneamos tu hoja de vida en 60 segundos. Sin costo."
                },
                "custom_css": ".s4-question { font-size: clamp(26px,5.5cqw,38px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; }"
            }
        ]
    },
    # ── 4. cosmic-ribbons + s27 ─────────────────────────────────────────────
    {
        "bg": "cosmic-ribbons",
        "system": "s27",
        "topic": "palabras-que-busca-bot",
        "pacing": ["hook", "silence", "solution", "cta"],
        "shared_layer": "geo-flow-wave",
        "slides": [
            {
                "id": "s1",
                "layout": "slide-typeset-poster",
                "layers": ["geo-flow-wave", "geo-neon-ring"],
                "decoratives": [{"id": "svg-starburst-spark", "position": "tr"}],
                "copy": {
                    "eyebrow": "WORQAI INSIGHT",
                    "headline": "No busca talento. Busca palabras.",
                    "footer_left": "@worqai",
                    "footer_right": "2026"
                },
                "custom_css": ".s1-display { font-size: clamp(36px,7.5cqw,60px); font-weight: 900; letter-spacing: -0.04em; line-height: 1.0; text-align: center; } .s1-eyebrow { letter-spacing: 0.2em; font-size: 12px; opacity: 0.85; }"
            },
            {
                "id": "s2",
                "layout": "slide-asymmetric-lockup",
                "layers": ["geo-flow-wave", "geo-starfield"],
                "copy": {
                    "kicker": "EL SILENCIO",
                    "headline": "El bot no sabe quien sos.",
                    "body": "Sabe si aparece 'Python', 'Scrum' o 'KPI'. Nada mas."
                },
                "custom_css": ".s2-headline { font-size: clamp(28px,6cqw,44px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; } .s2-body { opacity: 0.85; max-width: 32ch; font-size: 15px; }"
            },
            {
                "id": "s3",
                "layout": "slide-myth-vs-fact",
                "layers": ["geo-flow-wave", "glow-orb"],
                "decoratives": [{"id": "svg-starburst-burst", "position": "bl"}],
                "copy": {
                    "kicker": "MITO VS. REALIDAD",
                    "headline": "Lo que creis vs. lo que pasa",
                    "myth": "Un CV bonito impresiona al reclutador.",
                    "fact": "El reclutador nunca ve el CV bonito si el bot lo rechaza primero.",
                    "myth_label": "MITO",
                    "fact_label": "REALIDAD"
                },
                "custom_css": ".s3-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; } .s3-myth { opacity: 0.85; } .s3-fact { font-weight: 700; }"
            },
            {
                "id": "s4",
                "layout": "slide-cta",
                "layers": ["geo-flow-wave", "geo-neon-ring"],
                "decoratives": [{"id": "sub-stamp-circle", "text": "GRATIS"}],
                "copy": {
                    "question": "Tu CV tiene las palabras que el bot busca?",
                    "cta_keyword": "ESCANEAR",
                    "reward": "Te mostramos que falta. Sin costo, sin registro."
                },
                "custom_css": ".s4-question { font-size: clamp(26px,5.5cqw,38px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; }"
            }
        ]
    },
    # ── 5. digital-glass + s11 ──────────────────────────────────────────────
    {
        "bg": "digital-glass",
        "system": "s11",
        "topic": "tres-ajustes-doble-entrevistas",
        "pacing": ["hook", "data", "solution", "cta"],
        "shared_layer": "svg-blob-tr",
        "slides": [
            {
                "id": "s1",
                "layout": "slide-hook-lockup",
                "layers": ["svg-blob-tr", "geo-mesh-noise"],
                "decoratives": [{"id": "svg-starburst-spark", "position": "tr"}],
                "copy": {
                    "kicker": "RESULTADO REAL",
                    "headline": "3 cambios que duplican tus entrevistas",
                    "body": "No es magia. Es formato + palabras claras + estructura que el bot entiende.",
                    "swipe_prompt": "Desliza →"
                },
                "custom_css": ".s1-display { font-size: clamp(32px,6.5cqw,48px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; } .s1-body { opacity: 0.85; max-width: 40ch; }"
            },
            {
                "id": "s2",
                "layout": "slide-massive-number",
                "layers": ["svg-blob-tr", "geo-ribbon-flow"],
                "copy": {
                    "kicker": "ANTES / DESPUES",
                    "stat_number": "2.3x",
                    "headline": "Mas entrevistas con el mismo perfil",
                    "body": "Usuarios de WorqAI que aplicaron los 3 ajustes reportaron 2.3x mas llamadas de RRHH.",
                    "stat_context": "promedio reportado"
                },
                "custom_css": ".s2-stat { font-size: clamp(80px,16cqw,130px); font-weight: 900; letter-spacing: -0.05em; opacity: 0.14; } .s2-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; }"
            },
            {
                "id": "s3",
                "layout": "slide-before-after-stacked",
                "layers": ["svg-blob-tr", "glow-orb"],
                "decoratives": [{"id": "chrome-badge-stamp", "text": "WORQAI", "value": "TIP"}],
                "copy": {
                    "kicker": "ANTES / DESPUES",
                    "headline": "Mismo perfil, distinto parseo",
                    "before_label": "ANTES",
                    "before_text": "PDF con diseno creativo, tablas y columnas.",
                    "before_pct": 28,
                    "after_label": "DESPUES",
                    "after_text": ".docx simple, texto plano, palabras clave copiadas.",
                    "after_pct": 91
                },
                "custom_css": ".s3-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; } .s3-label { font-size: 11px; letter-spacing: 0.15em; }"
            },
            {
                "id": "s4",
                "layout": "slide-cta",
                "layers": ["svg-blob-tr", "geo-mesh-noise"],
                "decoratives": [{"id": "sub-stamp-circle", "text": "GRATIS"}],
                "copy": {
                    "question": "Listo para duplicar tus entrevistas?",
                    "cta_keyword": "AJUSTAR",
                    "reward": "Te guiamos paso a paso. Primera revision sin costo."
                },
                "custom_css": ".s4-question { font-size: clamp(26px,5.5cqw,38px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; }"
            }
        ]
    },
    # ── 6. dark-satin + s01 ─────────────────────────────────────────────────
    {
        "bg": "dark-satin",
        "system": "s01",
        "topic": "rrhh-no-dice-filtro",
        "pacing": ["hook", "diagnostic", "solution", "cta"],
        "shared_layer": "corner-frame",
        "slides": [
            {
                "id": "s1",
                "layout": "slide-frame-within-frame",
                "layers": ["corner-frame", "geo-topo-lines"],
                "decoratives": [{"id": "chrome-vertical-counter"}],
                "copy": {
                    "quote": "Tu CV puede ser excelente. Si el bot no lo lee, nadie lo sabra.",
                    "attribution": "Reclutador tech, anonimizado"
                },
                "custom_css": ".s1-quote { font-size: clamp(22px,4.5cqw,32px); font-weight: 400; font-style: italic; letter-spacing: -0.01em; line-height: 1.3; } .s1-attr { opacity: 0.75; font-size: 13px; margin-top: 16px; }"
            },
            {
                "id": "s2",
                "layout": "slide-terminal",
                "layers": ["corner-frame", "scan-lines"],
                "copy": {
                    "kicker": "DETRAS DEL FILTRO",
                    "headline": "Lo que RRHH no te dice",
                    "command": "ats --explain --verbose",
                    "tab_title": "worqai-insight",
                    "output_lines": [
                        {"type": "info", "text": "Tiempo promedio de revision humana: 6.2 segundos"},
                        {"type": "warn", "text": "Solo el 27% de CVs llega a esos 6 segundos"},
                        {"type": "err", "text": "Rechazo automatico: palabras clave < 60% match"},
                        {"type": "ok", "text": "El bot no tiene malicia. Tiene reglas."}
                    ]
                },
                "custom_css": ".s2-headline { font-size: clamp(22px,4.5cqw,32px); font-weight: 800; letter-spacing: -0.02em; }"
            },
            {
                "id": "s3",
                "layout": "slide-waffle-chart",
                "layers": ["corner-frame", "glow-orb"],
                "decoratives": [{"id": "svg-starburst-burst", "position": "bl"}],
                "copy": {
                    "kicker": "VISUAL",
                    "headline": "Solo 1 de 10 pasa ambos filtros",
                    "stat_number": "10%",
                    "filled": 10,
                    "context": "De 100 CVs, 10 llegan a entrevista. El resto mueren antes."
                },
                "custom_css": ".s3-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; } .s3-stat { font-size: clamp(48px,10cqw,80px); font-weight: 900; letter-spacing: -0.05em; }"
            },
            {
                "id": "s4",
                "layout": "slide-cta",
                "layers": ["corner-frame", "geo-topo-lines"],
                "decoratives": [{"id": "sub-stamp-circle", "text": "GRATIS"}],
                "copy": {
                    "question": "Queres saber si tu CV llega al humano?",
                    "cta_keyword": "PROBAR",
                    "reward": "Simulacion ATS en 60 segundos. Sin costo."
                },
                "custom_css": ".s4-question { font-size: clamp(26px,5.5cqw,38px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; }"
            }
        ]
    },
    # ── 7. futuristic-flow + s06 ────────────────────────────────────────────
    {
        "bg": "futuristic-flow",
        "system": "s06",
        "topic": "experiencia-valida-formato-no",
        "pacing": ["hook", "silence", "solution", "cta"],
        "shared_layer": "geo-starfield",
        "slides": [
            {
                "id": "s1",
                "layout": "slide-pull-quote",
                "layers": ["geo-starfield", "geo-neon-ring"],
                "decoratives": [{"id": "svg-starburst-spark", "position": "tr"}],
                "copy": {
                    "quote": "Tengo 8 anos de experiencia. El ATS me dio 12 puntos de 100.",
                    "attribution": "Usuario WorqAI, sector retail"
                },
                "custom_css": ".s1-quote { font-size: clamp(22px,4.5cqw,32px); font-weight: 400; font-style: italic; line-height: 1.3; } .s1-attr { opacity: 0.75; font-size: 13px; margin-top: 16px; }"
            },
            {
                "id": "s2",
                "layout": "slide-full-bleed-type",
                "layers": ["geo-starfield", "geo-mesh-noise"],
                "copy": {
                    "eyebrow": "WORQAI",
                    "headline": "Tu experiencia es valida. Tu formato, no.",
                    "sub": "El bot no juzga lo que hiciste. Juzga como lo escribiste."
                },
                "custom_css": ".s2-display { font-size: clamp(32px,7cqw,54px); font-weight: 900; letter-spacing: -0.04em; line-height: 1.0; } .s2-sub { opacity: 0.85; font-size: 15px; max-width: 36ch; margin-top: 20px; }"
            },
            {
                "id": "s3",
                "layout": "slide-before-after",
                "layers": ["geo-starfield", "glow-orb"],
                "decoratives": [{"id": "svg-starburst-burst", "position": "bl"}],
                "copy": {
                    "kicker": "ANTES / DESPUES",
                    "headline": "Mismo perfil, distinto resultado",
                    "before_items": ["PDF con columnas", "Titulos creativos", "Sin palabras clave"],
                    "after_items": [".docx lineal", "Titulos del puesto", "Verbos del aviso copiados"],
                    "before_score": "12",
                    "after_score": "89"
                },
                "custom_css": ".s3-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; } .s3-score { font-weight: 900; font-size: clamp(48px,10cqw,80px); letter-spacing: -0.04em; }"
            },
            {
                "id": "s4",
                "layout": "slide-cta",
                "layers": ["geo-starfield", "geo-neon-ring"],
                "decoratives": [{"id": "sub-stamp-circle", "text": "GRATIS"}],
                "copy": {
                    "question": "Tu experiencia se ve en tu CV como es?",
                    "cta_keyword": "REVISAR",
                    "reward": "Te mostramos si el bot entiende tu trayectoria. Sin costo."
                },
                "custom_css": ".s4-question { font-size: clamp(26px,5.5cqw,38px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; }"
            }
        ]
    },
    # ── 8. glass-panel + s25 ────────────────────────────────────────────────
    {
        "bg": "glass-panel",
        "system": "s25",
        "topic": "reclutador-vs-bot",
        "pacing": ["hook", "diagnostic", "solution", "cta"],
        "shared_layer": "geo-data-streaks",
        "slides": [
            {
                "id": "s1",
                "layout": "slide-side-by-side",
                "layers": ["geo-data-streaks", "grid-bg"],
                "copy": {
                    "kicker": "DOS JUECES",
                    "headline": "El reclutador busca talento. El bot, coincidencias.",
                    "left_content": "VS",
                    "body": "Uno lee intencion. El otro lee texto. Ganas si pasas los dos filtros."
                },
                "custom_css": ".s1-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; line-height: 1.1; } .s1-body { opacity: 0.85; max-width: 36ch; } .s1-left { font-size: clamp(48px,10cqw,80px); font-weight: 900; letter-spacing: -0.05em; }"
            },
            {
                "id": "s2",
                "layout": "slide-myth-vs-fact",
                "layers": ["geo-data-streaks", "geo-ribbon-flow"],
                "decoratives": [{"id": "svg-starburst-spark", "position": "tr"}],
                "copy": {
                    "kicker": "MITO VS. REALIDAD",
                    "headline": "Lo que creis vs. lo que pasa",
                    "myth": "Un CV bonito impresiona al reclutador.",
                    "fact": "El reclutador nunca ve el CV bonito si el bot lo rechaza primero.",
                    "myth_label": "MITO",
                    "fact_label": "REALIDAD"
                },
                "custom_css": ".s2-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; } .s2-myth { opacity: 0.85; } .s2-fact { font-weight: 700; }"
            },
            {
                "id": "s3",
                "layout": "slide-stat-row",
                "layers": ["geo-data-streaks", "glow-orb"],
                "decoratives": [{"id": "svg-starburst-burst", "position": "bl"}],
                "copy": {
                    "kicker": "DATOS",
                    "headline": "Los numeros no mienten",
                    "stats": [
                        {"num": "250+", "label": "CVs por puesto", "body": "Promedio en empresas medianas."},
                        {"num": "73%", "label": "Rechazo automatico", "body": "El bot filtra antes del humano."},
                        {"num": "6s", "label": "Tiempo humano", "body": "Segundos que el reclutador te dedica."}
                    ]
                },
                "custom_css": ".s3-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; } .s3-stat-num { font-weight: 900; font-size: clamp(36px,7cqw,56px); letter-spacing: -0.04em; }"
            },
            {
                "id": "s4",
                "layout": "slide-cta",
                "layers": ["geo-data-streaks", "grid-bg"],
                "decoratives": [{"id": "sub-stamp-circle", "text": "GRATIS"}],
                "copy": {
                    "question": "Tu CV gana los dos filtros?",
                    "cta_keyword": "COMPROBAR",
                    "reward": "Diagnostico ATS + checklist del reclutador. Gratis."
                },
                "custom_css": ".s4-question { font-size: clamp(26px,5.5cqw,38px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; }"
            }
        ]
    },
    # ── 9. galactic-dream + s21 ─────────────────────────────────────────────
    {
        "bg": "galactic-dream",
        "system": "s21",
        "topic": "cincuenta-a-cinco",
        "pacing": ["hook", "data", "solution", "cta"],
        "shared_layer": "geo-neon-ring",
        "slides": [
            {
                "id": "s1",
                "layout": "slide-tag-cloud",
                "layers": ["geo-neon-ring", "geo-starfield"],
                "decoratives": [{"id": "svg-starburst-spark", "position": "tr"}],
                "copy": {
                    "kicker": "EL FUNNEL",
                    "headline": "50 aplicaciones → 5 entrevistas",
                    "words": [
                        {"text": "APLICA", "size": 28, "x": 60, "y": 180, "opacity": 0.9},
                        {"text": "50 veces", "size": 18, "x": 200, "y": 140, "opacity": 0.7},
                        {"text": "El bot filtra", "size": 16, "x": 120, "y": 280, "opacity": 0.6},
                        {"text": "37 quedan", "size": 20, "x": 300, "y": 240, "opacity": 0.75},
                        {"text": "El humano elige", "size": 16, "x": 220, "y": 380, "opacity": 0.6},
                        {"text": "5 entrevistas", "size": 24, "x": 80, "y": 460, "opacity": 0.85}
                    ]
                },
                "custom_css": ".s1-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; } .s1-word { font-weight: 800; }"
            },
            {
                "id": "s2",
                "layout": "slide-waffle-chart",
                "layers": ["geo-neon-ring", "geo-pixel-grid"],
                "copy": {
                    "kicker": "VISUAL",
                    "headline": "Solo 1 de 10 pasa ambos filtros",
                    "stat_number": "10%",
                    "filled": 10,
                    "context": "De 100 CVs, 10 llegan a entrevista. El resto mueren antes."
                },
                "custom_css": ".s2-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; } .s2-stat { font-size: clamp(48px,10cqw,80px); font-weight: 900; letter-spacing: -0.05em; }"
            },
            {
                "id": "s3",
                "layout": "slide-icon-grid",
                "layers": ["geo-neon-ring", "glow-orb"],
                "decoratives": [{"id": "svg-starburst-burst", "position": "bl"}],
                "copy": {
                    "kicker": "COMO ESTAR EN EL 10%",
                    "headline": "4 movimientos que multiplican chances",
                    "tiles": [
                        {"icon": "target", "title": "Aplica con precision", "desc": "10 puestos bien elegidos > 50 al azar."},
                        {"icon": "lock", "title": "Formato limpio", "desc": "docx simple, sin tablas, sin imagenes."},
                        {"icon": "chart", "title": "Palabras clave", "desc": "Copia del aviso. No inventes."},
                        {"icon": "trophy", "title": "Numeros concretos", "desc": "% y $ en cada logro."}
                    ]
                },
                "custom_css": ".s3-headline { font-size: clamp(24px,5cqw,36px); font-weight: 900; letter-spacing: -0.02em; } .s3-tile-title { font-weight: 700; font-size: 14px; }"
            },
            {
                "id": "s4",
                "layout": "slide-cta",
                "layers": ["geo-neon-ring", "geo-starfield"],
                "decoratives": [{"id": "sub-stamp-circle", "text": "GRATIS"}],
                "copy": {
                    "question": "Queres pasar del 50 al 5?",
                    "cta_keyword": "OPTIMIZAR",
                    "reward": "Plan personalizado para tu perfil. Primera sesion gratis."
                },
                "custom_css": ".s4-question { font-size: clamp(26px,5.5cqw,38px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; }"
            }
        ]
    },
    # ── 10. blue-geometry + s17 ─────────────────────────────────────────────
    {
        "bg": "blue-geometry",
        "system": "s17",
        "topic": "cv-perfecto-no-pasa",
        "pacing": ["hook", "diagnostic", "solution", "cta"],
        "shared_layer": "pw-grid",
        "slides": [
            {
                "id": "s1",
                "layout": "slide-hook-lockup",
                "layers": ["pw-grid", "geo-circuit-trace"],
                "decoratives": [{"id": "svg-starburst-spark", "position": "tr"}],
                "copy": {
                    "kicker": "LA PARADOJA",
                    "headline": "Tu CV esta perfecto. Y por eso no pasa.",
                    "body": "Diseno editorial, tipografia cuidada, colores armonicos. El bot no ve ninguno.",
                    "swipe_prompt": "Desliza →"
                },
                "custom_css": ".s1-display { font-size: clamp(30px,6.5cqw,48px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; } .s1-body { opacity: 0.85; max-width: 40ch; }"
            },
            {
                "id": "s2",
                "layout": "slide-terminal",
                "layers": ["pw-grid", "scan-lines"],
                "copy": {
                    "kicker": "LO QUE VE EL BOT",
                    "headline": "Tu 'obra de arte' traducida a texto",
                    "command": "worqai --parse cv_diseno.pdf",
                    "tab_title": "worqai-parse",
                    "output_lines": [
                        {"type": "warn", "text": "Imagen de fondo detectada: ignorada"},
                        {"type": "err", "text": "Tabla de contacto: contenido no extraido"},
                        {"type": "err", "text": "Columna derecha: texto truncado"},
                        {"type": "info", "text": "Contenido recuperado: 34% del total"},
                        {"type": "err", "text": "Score final: 31/100 — below threshold"}
                    ]
                },
                "custom_css": ".s2-headline { font-size: clamp(22px,4.5cqw,32px); font-weight: 800; letter-spacing: -0.02em; }"
            },
            {
                "id": "s3",
                "layout": "slide-input-output",
                "layers": ["pw-grid", "glow-orb"],
                "decoratives": [{"id": "svg-starburst-burst", "position": "bl"}],
                "copy": {
                    "kicker": "EL PROBLEMA",
                    "headline": "Lo que envias vs. lo que lee el ATS",
                    "input_label": "Tu CV (se ve asi)",
                    "input_text": "Diseno visual con iconos, tablas de habilidades y graficos de progreso.",
                    "output_label": "El ATS lo lee asi",
                    "output_text": "[NOMBRE] [TEXTO SIN FORMATO] [DATOS PERDIDOS] Score: 28/100"
                },
                "custom_css": ".s3-headline { font-size: clamp(22px,4.5cqw,32px); font-weight: 800; letter-spacing: -0.02em; } .s3-panel-label { font-size: 11px; letter-spacing: 0.15em; text-transform: uppercase; opacity: 0.85; }"
            },
            {
                "id": "s4",
                "layout": "slide-cta",
                "layers": ["pw-grid", "geo-circuit-trace"],
                "decoratives": [{"id": "sub-stamp-circle", "text": "GRATIS"}],
                "copy": {
                    "question": "Tu CV perfecto sobrevive al bot?",
                    "cta_keyword": "ESCANEAR",
                    "reward": "Te decimos que porcentaje lee el ATS. Sin costo."
                },
                "custom_css": ".s4-question { font-size: clamp(26px,5.5cqw,38px); font-weight: 900; letter-spacing: -0.03em; line-height: 1.05; }"
            }
        ]
    },
]


def build_spec(cfg: dict) -> dict:
    slides = []
    for slide_cfg in cfg["slides"]:
        # prepend the AI background ID so resolve_geo() picks it up via resolve_ai_bg()
        layers = [cfg["bg"]] + slide_cfg["layers"]
        slide = {
            "id": slide_cfg["id"],
            "layout": slide_cfg["layout"],
            "layers": layers,
            "copy": slide_cfg["copy"],
        }
        if "decoratives" in slide_cfg:
            slide["decoratives"] = slide_cfg["decoratives"]
        if "custom_css" in slide_cfg:
            slide["custom_css"] = slide_cfg["custom_css"]
        slides.append(slide)

    return {
        "meta": {
            "system": cfg["system"],
            "aspect": "1:1",
            "slides": 4,
            "brand": "@worqai",
            "language": "es-CR",
            "topic": cfg["topic"],
            "density": "standard",
            "bg_recipe": "extracted",
            "continuity": ""
        },
        "pacing": cfg["pacing"],
        "slides": slides
    }


def main():
    for cfg in SPECS:
        spec = build_spec(cfg)
        filename = f"ai-bg-{cfg['topic']}-{cfg['system']}-spec.json"
        path = PRODUCTION / filename
        path.write_text(json.dumps(spec, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[WRITE] {path.name}")


if __name__ == "__main__":
    main()
