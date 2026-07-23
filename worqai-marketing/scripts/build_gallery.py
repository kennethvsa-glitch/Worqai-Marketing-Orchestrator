#!/usr/bin/env python3
"""
build_gallery.py — Renders isolated + context demos for all components + gallery/INDEX.html.

Run:
    py scripts/build_gallery.py

Output:
    gallery/INDEX.html
    gallery/01-geo-mesh-noise-component.html  (isolated — dark bg, component only)
    gallery/01-geo-mesh-noise-context.html    (in-context — real slide, real system)
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
GALLERY = ROOT / "gallery"

sys.path.insert(0, str(ROOT / "scripts"))
from render_carousel import render_carousel

# ─── Cleaned DEMOS array (122 items) ──────────────────────────────────────────
# Duplicates removed: geo-topo-lines, scan-lines, slide-cta-solo,
#   slide-before-after-col, glow-orb, zoom-rings, grid-bg, diag-band, blob-bg
# New CSS demos added: css-text-gradient, css-text-glow, css-text-stroke

DEMOS = [
    # ═══════════════════════════════════════════════════════════════════════
    # GEO LAYERS (42)
    # ═══════════════════════════════════════════════════════════════════════
    {"slug":"geo-mesh-noise","title":"Mesh Noise","tier":"1_geo","system":"s04","cat":"Geo","desc":"Animated soft mesh-gradient blob. Warm + light systems.",
     "showcase":{"layout":"slide-big-number","layers":["geo-mesh-noise","blob-bg"],
        "copy":{"kicker":"Mesh demo","stat_number":"82%","stat_context":"menos rigidez visual","headline":"Soft motion","body":"Capa orgánica que se mueve con el contenido."}}},
    {"slug":"geo-pixel-grid","title":"Pixel Grid","tier":"1_geo","system":"s29","cat":"Geo","desc":"Tight dot matrix. Cyberpunk + dark.",
     "showcase":{"layout":"slide-big-number","layers":["geo-pixel-grid","glow-orb"],
        "copy":{"kicker":"Pixel demo","stat_number":"60%","stat_context":"densidad puntual","headline":"Tech density","body":"Dot-matrix sin perspectiva 3D."}}},
    {"slug":"geo-conic-rays","title":"Conic Rays","tier":"1_geo","system":"s07","cat":"Geo","desc":"Conic sunburst. Brutalist + warm.",
     "showcase":{"layout":"slide-big-number","layers":["geo-conic-rays"],
        "copy":{"kicker":"Sunburst","stat_number":"45°","stat_context":"ángulo de impacto","headline":"Energía radial","body":"Rayos cónicos desde la esquina."}}},
    {"slug":"geo-chevron-stripe","title":"Chevron Stripe","tier":"1_geo","system":"s07","cat":"Geo","desc":"Diagonal repeating chevrons. Brutalist + dark.",
     "showcase":{"layout":"slide-hook-lockup","layers":["geo-chevron-stripe"],
        "copy":{"kicker":"Chevron","headline":"Ritmo gráfico\nen diagonal.","body":"Patrón repetido para identidad editorial."}}},
    {"slug":"geo-iso-grid","title":"Isometric Grid","tier":"1_geo","system":"s17","cat":"Geo","desc":"Isometric grid, no perspective rotation. Tech + dark.",
     "showcase":{"layout":"slide-big-number","layers":["geo-iso-grid"],
        "copy":{"kicker":"Iso grid","stat_number":"3D","stat_context":"sin distorsión","headline":"Grilla isométrica","body":"Variante plana del perspective grid."}}},
    {"slug":"geo-paper-texture","title":"Paper Texture","tier":"1_geo","system":"s05","cat":"Geo","desc":"Organic paper fiber. Light editorial.",
     "showcase":{"layout":"slide-pull-quote-author","layers":["geo-paper-texture"],
        "copy":{"kicker":"Editorial","quote":"El papel cambia el peso de las palabras.","author":"Studio Note","role":"Brand voice"}}},
    {"slug":"geo-halftone","title":"Halftone","tier":"1_geo","system":"s25","cat":"Geo","desc":"Print-style halftone dots. Brutalist + editorial.",
     "showcase":{"layout":"slide-hook-lockup","layers":["geo-halftone"],
        "copy":{"kicker":"Print","headline":"Estética de\nimprenta digital.","body":"Gradiente de puntos con máscara diagonal."}}},
    {"slug":"geo-ribbon-flow","title":"Ribbon Flow","tier":"1_geo","system":"s04","cat":"Geo","desc":"Bezier ribbons. Warm + light.",
     "showcase":{"layout":"slide-pull-quote-author","layers":["geo-ribbon-flow"],
        "copy":{"kicker":"Flow","quote":"Curvas suaves bajan la ansiedad del lector.","author":"Tone Note","role":"UX"}}},
    {"slug":"geo-circuit-trace","title":"Circuit Trace","tier":"1_geo","system":"s29","cat":"Geo","desc":"PCB circuit lines — cyberpunk only.",
     "showcase":{"layout":"slide-terminal","layers":["geo-circuit-trace","scan-lines"],
        "copy":{"kicker":"Cyberpunk only","headline":"PCB traces","output_lines":[{"type":"ok","text":"Circuit active"},{"type":"warn","text":"Node n2 hot"},{"type":"ok","text":"ready"}]}}},
    {"slug":"geo-starfield","title":"Starfield","tier":"1_geo","system":"s17","cat":"Geo","desc":"Sparse star/dot scatter. Dark + cyberpunk.",
     "showcase":{"layout":"slide-pull-quote-author","layers":["geo-starfield","glow-orb"],
        "copy":{"kicker":"Starfield","quote":"Ruido visual disperso, no denso.","author":"Background Note","role":"Atmósfera"}}},
    {"slug":"geo-gradient-bands","title":"Gradient Bands","tier":"1_geo","system":"s05","cat":"Geo","desc":"Horizontal stripe gradient. Warm + light editorial.",
     "showcase":{"layout":"slide-hook-lockup","layers":["geo-gradient-bands"],
        "copy":{"kicker":"Bands","headline":"Bandas\nhorizontales.","body":"Sutil ritmo editorial sin grid pesado."}}},
    {"slug":"geo-contour-flow","title":"Contour Flow","tier":"1_geo","system":"s17","cat":"Geo","desc":"Flowing topographic contour lines. Dark + brutalist editorial.",
     "showcase":{"layout":"slide-big-number","layers":["geo-contour-flow"],
        "copy":{"kicker":"Geo v3","stat_number":"06","stat_context":"líneas de contorno","headline":"Mapa fluido","body":"Curvas suaves que crean profundidad sin ruido."}}},
    {"slug":"geo-perspective-grid","title":"Perspective Grid","tier":"1_geo","system":"s29","cat":"Geo","desc":"3D wireframe receding to vanishing point. PLAYWRIGHT ONLY.",
     "showcase":{"layout":"slide-terminal","layers":["geo-perspective-grid","scan-lines"],
        "copy":{"kicker":"3D layer","headline":"Perspectiva","command":"ats-check --depth","output_lines":[{"type":"ok","text":"Grid render OK"},{"type":"warn","text":"Playwright only"}]}}},
    {"slug":"geo-hex-mesh","title":"Hex Mesh","tier":"1_geo","system":"s17","cat":"Geo","desc":"Hexagonal tessellation. Molecular / honeycomb pattern.",
     "showcase":{"layout":"slide-hook-lockup","layers":["geo-hex-mesh"],
        "copy":{"kicker":"Molecular","headline":"Hexágonos.","body":"Patrón de panal para tech y biotech."}}},
    {"slug":"geo-constellation","title":"Constellation","tier":"1_geo","system":"s17","cat":"Geo","desc":"Particle network with dots and connections. Static SVG.",
     "showcase":{"layout":"slide-big-number","layers":["geo-constellation"],
        "copy":{"kicker":"Network","stat_number":"13","stat_context":"nodos conectados","headline":"Red estática","body":"Constelación pre-generada, no Canvas."}}},
    {"slug":"geo-neon-ring","title":"Neon Ring","tier":"1_geo","system":"s16","cat":"Geo","desc":"Glowing portal/aura ring with multi-layer SVG circles.",
     "showcase":{"layout":"slide-cta","layers":["geo-neon-ring","glow-orb"],
        "copy":{"question":"¿Aprobás el anillo?","cta_keyword":"RING","reward":"Portal glow con 4 capas de círculos SVG."}}},
    {"slug":"geo-bokeh","title":"Bokeh","tier":"1_geo","system":"s04","cat":"Geo","desc":"Atmospheric lens blur orbs. CSS radial-gradient + blur.",
     "showcase":{"layout":"slide-pull-quote-author","layers":["geo-bokeh"],
        "copy":{"kicker":"Atmosphere","quote":"Desenfoque que crea profundidad sin competir con el texto.","author":"Depth Note","role":"Atmósfera"}}},
    {"slug":"geo-scan-lines","title":"Scan Lines","tier":"1_geo","system":"s29","cat":"Geo","desc":"Subtle CRT scan-line texture overlay. All renderers.",
     "showcase":{"layout":"slide-terminal","layers":["geo-scan-lines"],
        "copy":{"kicker":"CRT","headline":"Líneas de scan","command":"scan --mode subtle","output_lines":[{"type":"ok","text":"3px spacing"},{"type":"info","text":"Mix-blend: overlay"}]}}},
    {"slug":"geo-chromatic-edge","title":"Chromatic Edge","tier":"1_geo","system":"s17","cat":"Geo","desc":"RGB lens aberration bleed at viewport edges. CSS only.",
     "showcase":{"layout":"slide-hook-lockup","layers":["geo-chromatic-edge"],
        "copy":{"kicker":"Lens","headline":"Aberración cromática.","body":"Degradados rojo/azul en los bordes. Efecto óptico sutil."}}},
    {"slug":"geo-data-streaks","title":"Data Streaks","tier":"1_geo","system":"s29","cat":"Geo","desc":"Static diagonal data stream lines. SVG stroke elements.",
     "showcase":{"layout":"slide-big-number","layers":["geo-data-streaks"],
        "copy":{"kicker":"Stream","stat_number":"19","stat_context":"líneas diagonales","headline":"Flujo de datos","body":"Líneas estáticas a 45° con opacidad variable."}}},
    {"slug":"geo-liquid-morph","title":"Liquid Morph","tier":"1_geo","system":"s04","cat":"Geo","desc":"Overlapping blurred circles creating metaball intersections. SVG filter.",
     "showcase":{"layout":"slide-pull-quote-author","layers":["geo-liquid-morph"],
        "copy":{"kicker":"Metaball","quote":"Círculos borrosos que se funden entre sí.","author":"Filter Note","role":"SVG feGaussianBlur"}}},
    {"slug":"geo-blob-bg","title":"Blob Background","tier":"1_geo","system":"s04","cat":"Geo","desc":"CSS radial ellipse blur — base layer for warm/organic systems.",
     "showcase":{"layout":"slide-hook-lockup","layers":["blob-bg","vol-light"],
        "copy":{"kicker":"Layer clásico","headline":"Blob\nde fondo.","body":"Elipse suavizada — base de los sistemas warm y orgánicos."}}},
    {"slug":"geo-glow-orb","title":"Glow Orb","tier":"1_geo","system":"s17","cat":"Geo","desc":"Central radial glow sphere. Dark + cyberpunk systems.",
     "showcase":{"layout":"slide-big-number","layers":["glow-orb"],
        "copy":{"kicker":"Acento","stat_number":"01","stat_context":"esfera de acento central","headline":"Foco luminoso","body":"Radial gradient centrado. Dark + cyberpunk."}}},
    {"slug":"geo-zoom-rings","title":"Zoom Rings","tier":"1_geo","system":"s29","cat":"Geo","desc":"Concentric expanding rings. Cyberpunk only.",
     "showcase":{"layout":"slide-hook-lockup","layers":["zoom-rings","glow-orb"],
        "copy":{"kicker":"Profundidad","headline":"Anillos\nconcéntricos.","body":"Tres círculos que crean campo visual en perspectiva."}}},
    {"slug":"geo-grid-bg","title":"Grid Background","tier":"1_geo","system":"s07","cat":"Geo","desc":"Flat CSS grid. Brutalist + dark editorial base.",
     "showcase":{"layout":"slide-hook-lockup","layers":["grid-bg"],
        "copy":{"kicker":"Base brutalist","headline":"Grilla\nde fondo.","body":"Módulo base para sistemas tipográficos fuertes."}}},
    {"slug":"geo-diag-band","title":"Diagonal Band","tier":"1_geo","system":"s05","cat":"Geo","desc":"Single diagonal accent band. Light editorial only.",
     "showcase":{"layout":"slide-pull-quote-author","layers":["diag-band"],
        "copy":{"kicker":"Editorial","quote":"La banda diagonal rompe la monotonía sin competir con el texto.","author":"Layer Note","role":"Light editorial"}}},
    {"slug":"pw-grid","title":"PW Grid","tier":"1_geo","system":"s29","cat":"Geo","desc":"Cyberpunk wireframe background. Dark systems only.",
     "showcase":{"layout":"slide-big-number","layers":["pw-grid"],
        "copy":{"kicker":"Grid","stat_number":"01","stat_context":"wireframe base","headline":"Estructura digital"}}},
    {"slug":"vol-light","title":"Vol Light","tier":"1_geo","system":"s17","cat":"Geo","desc":"Volumetric glow beams. Atmospheric depth.",
     "showcase":{"layout":"slide-big-number","layers":["vol-light"],
        "copy":{"kicker":"Depth","stat_number":"8","stat_context":"haces de luz","headline":"Volumetría"}}},
    {"slug":"svg-blob-tr","title":"SVG Blob TR","tier":"1_geo","system":"s04","cat":"Geo","desc":"v2: real SVG bezier blob, top-right. Replaces ellipse blob-bg.",
     "showcase":{"layout":"slide-hook-lockup","layers":["svg-blob-tr"],
        "copy":{"kicker":"Blob v2","headline":"Forma orgánica real.","body":"SVG bezier en vez de ellipse + blur. 100% capturable."}}},
    {"slug":"svg-blob-bl","title":"SVG Blob BL","tier":"1_geo","system":"s04","cat":"Geo","desc":"v2: SVG blob, bottom-left.",
     "showcase":{"layout":"slide-big-number","layers":["svg-blob-bl"],
        "copy":{"kicker":"Blob BL","stat_number":"02","stat_context":"variante inferior","headline":"Blob abajo"}}},
    {"slug":"svg-blob-center","title":"SVG Blob Center","tier":"1_geo","system":"s04","cat":"Geo","desc":"v2: SVG blob centered behind hero. Low opacity.",
     "showcase":{"layout":"slide-pull-quote-author","layers":["svg-blob-center"],
        "copy":{"kicker":"Center","quote":"Centrado, baja opacidad, máxima legibilidad.","author":"Center Note","role":"v2 blob"}}},
    {"slug":"svg-blob-asymmetric","title":"SVG Blob Asymmetric","tier":"1_geo","system":"s04","cat":"Geo","desc":"v2: aggressive asymmetric blob, top-right.",
     "showcase":{"layout":"slide-hook-lockup","layers":["svg-blob-asymmetric"],
        "copy":{"kicker":"Asymmetric","headline":"Asimetría agresiva.","body":"Para marcas que rompen el grid."}}},
    {"slug":"svg-blob-scattered","title":"SVG Blob Scattered","tier":"1_geo","system":"s04","cat":"Geo","desc":"v2: three scattered small blobs as atmosphere.",
     "showcase":{"layout":"slide-big-number","layers":["svg-blob-scattered"],
        "copy":{"kicker":"Scattered","stat_number":"3","stat_context":"blobs dispersos","headline":"Atmósfera ligera"}}},
    {"slug":"svg-blob-angular","title":"SVG Blob Angular","tier":"1_geo","system":"s07","cat":"Geo","desc":"v3: sharp 8-point polygon. Brutalist/dark edge tension.",
     "showcase":{"layout":"slide-hook-lockup","layers":["svg-blob-angular"],
        "copy":{"kicker":"Angular","headline":"Puntos afilados.","body":"Sin curvas. Solo tensión y ángulos."}}},
    {"slug":"svg-blob-crystal","title":"SVG Blob Crystal","tier":"1_geo","system":"s29","cat":"Geo","desc":"v3: faceted gem-like shards. Cyberpunk/tech premium.",
     "showcase":{"layout":"slide-big-number","layers":["svg-blob-crystal"],
        "copy":{"kicker":"Crystal","stat_number":"12","stat_context":"facetas","headline":"Gema digital"}}},
    {"slug":"svg-blob-wave","title":"SVG Blob Wave","tier":"1_geo","system":"s04","cat":"Geo","desc":"v3: smooth horizontal S-curve. Warm/light continuity.",
     "showcase":{"layout":"slide-pull-quote-author","layers":["svg-blob-wave"],
        "copy":{"kicker":"Wave","quote":"Una curva que fluye de izquierda a derecha.","author":"Flow Note","role":"Continuity"}}},
    {"slug":"svg-blob-arch","title":"SVG Blob Arch","tier":"1_geo","system":"s17","cat":"Geo","desc":"v3: architectural column/vault. Art deco, authority.",
     "showcase":{"layout":"slide-hook-lockup","layers":["svg-blob-arch"],
        "copy":{"kicker":"Arch","headline":"Autoridad estructural.","body":"Forma de columna para contenido con peso."}}},
    {"slug":"svg-blob-splatter","title":"SVG Blob Splatter","tier":"1_geo","system":"s04","cat":"Geo","desc":"v3: irregular paint-splatter edges. Creative energy.",
     "showcase":{"layout":"slide-big-number","layers":["svg-blob-splatter"],
        "copy":{"kicker":"Splatter","stat_number":"99","stat_context":"gotas de energía","headline":"Caos controlado"}}},
    {"slug":"svg-blob-ribbon","title":"SVG Blob Ribbon","tier":"1_geo","system":"s04","cat":"Geo","desc":"v3: twisted Möbius-style loop. Modern SaaS, motion.",
     "showcase":{"layout":"slide-pull-quote-author","layers":["svg-blob-ribbon"],
        "copy":{"kicker":"Ribbon","quote":"Un loop infinito que sugiere transformación.","author":"Motion Note","role":"SaaS"}}},
    {"slug":"geo-flow-wave","title":"Flow Wave","tier":"1_geo","system":"s17","cat":"Geo","desc":"v3: sine-wave line spanning slide. Use with continuity:wave.",
     "showcase":{"layout":"slide-big-number","layers":["geo-flow-wave"],
        "copy":{"kicker":"Flow","stat_number":"~","stat_context":"onda continua","headline":"Sinusoide"}}},
    {"slug":"geo-flow-arrow","title":"Flow Arrow","tier":"1_geo","system":"s17","cat":"Geo","desc":"v3: large dashed arrow entering left. Progression signal.",
     "showcase":{"layout":"slide-hook-lockup","layers":["geo-flow-arrow"],
        "copy":{"kicker":"Arrow","headline":"Progresión implícita.","body":"Una flecha que apunta hacia adelante sin palabras."}}},
    {"slug":"geo-flow-data","title":"Flow Data","tier":"1_geo","system":"s29","cat":"Geo","desc":"v3: dotted particle trail with nodes. Tech continuity.",
     "showcase":{"layout":"slide-terminal","layers":["geo-flow-data","pw-grid"],
        "copy":{"kicker":"Pipeline","headline":"Datos en movimiento","command":"flow --status","output_lines":[{"type":"ok","text":"● Node 1 active"},{"type":"ok","text":"● Node 2 active"},{"type":"warn","text":"○ Node 3 idle"}]}}},

    # ═══════════════════════════════════════════════════════════════════════
    # CHROME (3)
    # ═══════════════════════════════════════════════════════════════════════
    {"slug":"chrome-vertical-counter","title":"Vertical Counter","tier":"2_chrome","system":"s05","cat":"Chrome","desc":"Rotated counter on right edge. Light editorial.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Demo","headline":"Contador\nvertical.","body":"Mirá el borde derecho — rotado 90°."},
        "extras":'<div class="chrome-vertical-counter">Issue 03 · 2026</div>'}},
    {"slug":"chrome-badge-stamp","title":"Badge Stamp","tier":"2_chrome","system":"s17","cat":"Chrome","desc":"Wax-seal style circular stamp. Universal.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Promo","headline":"Sello\ncircular.","body":"Identifica oferta, categoría o urgencia."},
        "extras":'<div class="chrome-badge-stamp"><div class="stamp-label">Nuevo</div><div class="stamp-value">FREE</div><div class="stamp-foot">audit</div></div>'}},
    {"slug":"chrome-header-bar","title":"Header Bar","tier":"2_chrome","system":"s05","cat":"Chrome","desc":"Magazine top bar. Light editorial only.",
     "showcase":{"layout":"slide-pull-quote-author","copy":{"kicker":"","quote":"Top bar tipo editorial impreso.","author":"Layout","role":"Magazine"},
        "extras":'<div class="chrome-header-bar"><div class="header-logo">WORQAI</div><div class="header-date">2026 · Issue 03</div></div>'}},

    # ═══════════════════════════════════════════════════════════════════════
    # LAYOUTS (52)
    # ═══════════════════════════════════════════════════════════════════════
    {"slug":"slide-myth-vs-fact","title":"Myth vs Fact","tier":"3_layout","system":"s17","cat":"Layout","desc":"Speech-bubble myth + fact callout.",
     "showcase":{"layout":"slide-myth-vs-fact","copy":{"kicker":"Educación","headline":"Lo que creés vs lo que pasa.",
        "myth":"Mandar 200 aplicaciones al mes funciona.","fact":"Tres aplicaciones bien hechas convierten más que cien spam."}}},
    {"slug":"slide-step-flow","title":"Step Flow","tier":"3_layout","system":"s07","cat":"Layout","desc":"Horizontal 3-4 step process with arrows.",
     "showcase":{"layout":"slide-step-flow","copy":{"kicker":"Proceso","headline":"De CV a entrevista en 4 pasos.",
        "steps":[{"title":"Scan ATS","desc":"Detectamos fallas."},{"title":"Reescritura","desc":"Bullets cuantificados."},{"title":"Optimizar","desc":"Keywords del puesto."},{"title":"Enviar","desc":"Aplicación final."}]}}},
    {"slug":"slide-comparison-table","title":"Comparison Table","tier":"3_layout","system":"s05","cat":"Layout","desc":"2-3 col matrix with checks.",
     "showcase":{"layout":"slide-comparison-table","copy":{"kicker":"Comparativa","headline":"Plantilla gratis vs Profile Pro.",
        "headers":["Feature","Free","Pro"],"rows":[["ATS scan","✗","✓"],["1-1 review","✗","✓"],["LinkedIn","✗","✓"],["Tiempo","2h","48h"]]}}},
    {"slug":"slide-faq-stack","title":"FAQ Stack","tier":"3_layout","system":"s17","cat":"Layout","desc":"Q&A stack for objection handling.",
     "showcase":{"layout":"slide-faq-stack","copy":{"kicker":"Dudas frecuentes","headline":"Lo que más nos preguntan.",
        "faqs":[{"q":"¿Cuánto demora?","a":"48 horas desde que mandás tu CV actual."},{"q":"¿Sirve para LATAM?","a":"Sí — optimizado para ATS regionales."},{"q":"¿Y si no me gusta?","a":"Una ronda de revisión incluida."}]}}},
    {"slug":"slide-quote-cascade","title":"Quote Cascade","tier":"3_layout","system":"s17","cat":"Layout","desc":"Multiple short testimonials.",
     "showcase":{"layout":"slide-quote-cascade","copy":{"kicker":"Resultados","headline":"Lo que dicen los clientes.",
        "quotes":[{"text":"De 0 a 4 entrevistas en 2 semanas.","attr":"Carlos M · QA"},{"text":"Cambió cómo veo mi propio CV.","attr":"Sofía R · PM"},{"text":"El reporte ATS me ahorró meses.","attr":"Luis D · Data"},{"text":"Vale cada peso.","attr":"Andrea P · UX"}]}}},
    {"slug":"slide-bento-grid","title":"Bento Grid","tier":"3_layout","system":"s17","cat":"Layout","desc":"2x2 or 3x2 bento cards.",
     "showcase":{"layout":"slide-bento-grid","copy":{"kicker":"Incluido","headline":"Todo lo que recibís.","grid":"g-2x2",
        "tiles":[{"label":"01","title":"CV ATS","body":"PDF + DOCX optimizado."},{"label":"02","title":"LinkedIn","body":"Headline + About + Skills."},{"label":"03","title":"Reporte","body":"Score detallado por sección."},{"label":"04","title":"Soporte","body":"Una ronda de revisión.","accent":True}]}}},
    {"slug":"slide-timeline","title":"Timeline","tier":"3_layout","system":"s17","cat":"Layout","desc":"Vertical timeline with milestones.",
     "showcase":{"layout":"slide-timeline","copy":{"kicker":"Roadmap","headline":"Tu carrera, mes a mes.",
        "events":[{"date":"Día 0","title":"CV actual","desc":"Score ATS 12/100."},{"date":"Día 2","title":"Reescritura","desc":"Score 84/100."},{"date":"Día 14","title":"Primera entrevista","desc":"3 procesos activos."},{"date":"Día 30","title":"Oferta","desc":"+22% salario base."}]}}},
    {"slug":"slide-stat-row","title":"Stat Row","tier":"3_layout","system":"s17","cat":"Layout","desc":"3 stat cards side-by-side.",
     "showcase":{"layout":"slide-stat-row","copy":{"kicker":"Datos 2025","headline":"El estado del mercado LATAM.",
        "stats":[{"num":"75","unit":"%","label":"Fallan ATS","body":"CVs con tablas o columnas."},{"num":"6","unit":"s","label":"Lectura","body":"Tiempo promedio reclutador."},{"num":"3","unit":"x","label":"Más entrevistas","body":"Con CV optimizado."}],"source":"Análisis interno WorqAI 2025"}}},
    {"slug":"slide-pull-quote-author","title":"Pull Quote + Author","tier":"3_layout","system":"s05","cat":"Layout","desc":"Editorial pull-quote with author block.",
     "showcase":{"layout":"slide-pull-quote-author","copy":{"kicker":"Testimonio","quote":"Pensé que mi CV era el problema. Era el formato.","author":"Carlos Méndez","role":"Senior QA · 2026"}}},
    {"slug":"slide-warning-banner","title":"Warning Banner","tier":"3_layout","system":"s17","cat":"Layout","desc":"Single alert card, sparse text — high impact.",
     "showcase":{"layout":"slide-warning-banner","copy":{"icon":"!","headline":"Tu CV <em>nunca</em> fue leído.","body":"El ATS lo rechazó antes de llegar a un humano."}}},
    {"slug":"slide-icon-grid","title":"Icon Grid","tier":"3_layout","system":"s17","cat":"Layout","desc":"6 icon+label tiles.",
     "showcase":{"layout":"slide-icon-grid","copy":{"kicker":"Cobertura","headline":"Optimizado para todos los ATS.",
        "tiles":[{"icon":"W","title":"Workday","desc":"Más usado en US"},{"icon":"T","title":"Taleo","desc":"Banca LATAM"},{"icon":"G","title":"Greenhouse","desc":"Startups"},{"icon":"L","title":"Lever","desc":"Tech medio"},{"icon":"I","title":"iCIMS","desc":"Retail"},{"icon":"S","title":"SAP","desc":"Corporativo"}]}}},
    {"slug":"slide-progress-bars","title":"Progress Bars","tier":"3_layout","system":"s17","cat":"Layout","desc":"Horizontal bars showing metric improvements.",
     "showcase":{"layout":"slide-progress-bars","copy":{"kicker":"Resultado","headline":"Antes vs Después del rewrite.",
        "bars":[{"label":"Score ATS","value":"+72","pct":84},{"label":"Keywords match","value":"+58","pct":72},{"label":"Entrevistas/mes","value":"+4","pct":60}],"source":"Cohorte 50 clientes Q1 2026"}}},
    {"slug":"slide-list-numbered","title":"Numbered List","tier":"3_layout","system":"s17","cat":"Layout","desc":"Large ranked numbered list (top 5).",
     "showcase":{"layout":"slide-list-numbered","copy":{"kicker":"Top 5","headline":"Errores que matan tu CV.",
        "items":[{"title":"Foto","desc":"El ATS la ignora, ocupa espacio."},{"title":"Columnas","desc":"Parseo en paralelo falla."},{"title":"Fuentes raras","desc":"Se corrompen al extraer texto."},{"title":"Tablas","desc":"La 2da columna desaparece."},{"title":"PDFs escaneados","desc":"Imagen, no texto leíble."}]}}},
    {"slug":"slide-data-viz-donut","title":"Donut Chart","tier":"3_layout","system":"s17","cat":"Layout","desc":"Donut + center number + legend.",
     "showcase":{"layout":"slide-data-viz-donut","copy":{"percent":75,"center_label":"falla ATS","kicker":"Datos","headline":"3 de 4 CVs rebotan.",
        "body":"En LATAM el problema es peor que en US por uso de plantillas no estándar.",
        "legend":[{"label":"Tablas","value":"42%","color":"var(--accent)"},{"label":"Foto/columnas","value":"23%","color":"#ff7eb3"},{"label":"Otros","value":"10%","color":"#feca57"}],"source":"Jobscan benchmark"}}},
    {"slug":"slide-typeset-poster","title":"Typeset Poster","tier":"3_layout","system":"s07","cat":"Layout","desc":"Type-as-art editorial poster.",
     "showcase":{"layout":"slide-typeset-poster","copy":{"eyebrow":"Issue 03 · Brutalist","headline":"<span class='strike-line'>Aplicar más</span><br><span class='accent-line'>aplicar mejor.</span>","footer_left":"@worqai","footer_right":"03/2026"}}},
    {"slug":"slide-waffle-chart","title":"Waffle Chart","tier":"3_layout","system":"s17","cat":"Layout","desc":"10×10 proportion grid. N cells filled with accent glow.",
     "showcase":{"layout":"slide-waffle-chart","layers":["geo-contour-flow"],
        "copy":{"kicker":"Data viz","stat_number":"73%","label":"RECHAZADOS","filled":73,"headline":"de CVs eliminados antes de revisión humana","context":"El ATS filtra automáticamente"}}},
    {"slug":"slide-input-output","title":"Input / Output","tier":"3_layout","system":"s17","cat":"Layout","desc":"Side-by-side ATS demo: human-readable vs garbled.",
     "showcase":{"layout":"slide-input-output","layers":["geo-data-streaks"],
        "copy":{"kicker":"Diagnóstico","headline":"El ATS lee de izquierda a derecha","input_label":"LO QUE ESCRIBISTE","input_text":"EXPERIENCIA | SKILLS | Ingeniera de Datos","output_label":"LO QUE VE EL ATS","output_text":"EXPERIENCIASKILLSIngenieradeDatos"}}},
    {"slug":"slide-before-after-stacked","title":"Before/After Stacked","tier":"3_layout","system":"s17","cat":"Layout","desc":"Stacked panels with VS badge and progress bars.",
     "showcase":{"layout":"slide-before-after-stacked","layers":["geo-hex-mesh"],
        "copy":{"kicker":"Transformación","headline":"Antes vs. Después","before_label":"CV CON COLUMNAS","before_text":"El ATS ve caos estructural.","before_pct":3,"after_label":"CV OPTIMIZADO ATS PURO","after_text":"Texto plano, 100% legible.","after_pct":98}}},
    {"slug":"slide-proof","title":"Social Proof","tier":"3_layout","system":"s17","cat":"Layout","desc":"Testimonial card + stat result + mechanism block.",
     "showcase":{"layout":"slide-proof",
        "copy":{"kicker":"Resultado","headline":"De 0 a 4 entrevistas.","quote":"Cambié el formato ATS y empezaron a llamarme en 2 semanas.","attribution":"Carlos M · QA Senior","stat_number":"+4","stat_context":"entrevistas en 14 días","body":"Keywords correctas + estructura plana sin tablas."}}},
    {"slug":"slide-tip-blocks","title":"Tip Blocks","tier":"3_layout","system":"s17","cat":"Layout","desc":"3 colored tip blocks: bad / neutral / good.",
     "showcase":{"layout":"slide-tip-blocks",
        "copy":{"kicker":"Diagnóstico","headline":"3 niveles de CV.",
           "tips":[{"problem":"Crítico","fix":"Tablas, fotos, columnas — falla ATS automáticamente."},{"problem":"Puede mejorar","fix":"Texto sin keywords del puesto específico."},{"problem":"Optimizado","fix":"Plano, cuantificado, con keywords exactas."}]}}},
    {"slug":"slide-massive-number","title":"Massive Number","tier":"3_layout","system":"s17","cat":"Layout","desc":"Oversized single stat — dominant typographic element.",
     "showcase":{"layout":"slide-massive-number",
        "copy":{"kicker":"Dato 2025","stat_number":"75%","stat_context":"CVs rechazados por ATS","headline":"antes de llegar a un humano.","body":"No es el reclutador. Es el filtro automático.","source":"Análisis interno WorqAI 2025"}}},
    {"slug":"slide-full-bleed-type","title":"Full Bleed Type","tier":"3_layout","system":"s07","cat":"Layout","desc":"Typography as the full canvas — editorial poster format.",
     "showcase":{"layout":"slide-full-bleed-type",
        "copy":{"eyebrow":"WorqAI · 2026","headline":"Tu CV\nmerece\nmás.","footer_left":"@worqai","footer_right":"03/2026"}}},
    {"slug":"slide-diagonal-split","title":"Diagonal Split","tier":"3_layout","system":"s17","cat":"Layout","desc":"Diagonal band dividing content zone and accent stat.",
     "showcase":{"layout":"slide-diagonal-split",
        "copy":{"kicker":"Contraste","headline":"Dos zonas,\nun mensaje.","body":"Cuerpo en zona principal, stat en el acento diagonal.","stat_number":"84","stat_context":"score ATS promedio post-rewrite"}}},
    {"slug":"slide-asymmetric-lockup","title":"Asymmetric Lockup","tier":"3_layout","system":"s05","cat":"Layout","desc":"Off-center type composition — editorial asymmetry.",
     "showcase":{"layout":"slide-asymmetric-lockup",
        "copy":{"kicker":"Editorial","headline":"Asimetría\nintencional.","body":"La tensión entre márgenes hace que el ojo no descanse."}}},
    {"slug":"slide-type-over-shape","title":"Type Over Shape","tier":"3_layout","system":"s04","cat":"Layout","desc":"Large typography floating over an organic blob or shape.",
     "showcase":{"layout":"slide-type-over-shape","layers":["blob-bg"],
        "copy":{"kicker":"Contraste","headline":"Texto sobre\nforma orgánica.","body":"La forma actúa como fondo activo, no decoración pasiva."}}},
    {"slug":"slide-stacked-type","title":"Stacked Type","tier":"3_layout","system":"s07","cat":"Layout","desc":"Multiple weight/size type layers stacked vertically.",
     "showcase":{"layout":"slide-stacked-type",
        "copy":{"kicker":"Tipografía","headline":"Capas\nde texto\nsuperpuestas.","body":"Contraste de peso y tamaño en eje vertical."}}},
    {"slug":"slide-corner-manifesto","title":"Corner Manifesto","tier":"3_layout","system":"s07","cat":"Layout","desc":"Strong editorial text anchored to a corner of the canvas.",
     "showcase":{"layout":"slide-corner-manifesto",
        "copy":{"kicker":"Manifiesto","headline":"El CV que\nnadie lee\nes el que\nnadie optimizó.","body":""}}},
    {"slug":"slide-data-wall","title":"Data Wall","tier":"3_layout","system":"s17","cat":"Layout","desc":"Dense grid of stat cards — data dashboard aesthetic.",
     "showcase":{"layout":"slide-data-wall",
        "copy":{"kicker":"Dashboard","headline":"Métricas clave.",
           "stats":[{"number":"75","unit":"%","label":"Falla ATS"},{"number":"6","unit":"s","label":"Tiempo lectura"},{"number":"84","unit":"","label":"Score óptimo"},{"number":"3","unit":"x","label":"Más entrevistas"},{"number":"48","unit":"h","label":"Entrega"},{"number":"2K","unit":"+","label":"Usuarios"}]}}},
    {"slug":"slide-side-by-side","title":"Side by Side","tier":"3_layout","system":"s17","cat":"Layout","desc":"Large stat on left, text content on right.",
     "showcase":{"layout":"slide-side-by-side",
        "copy":{"left_content":"75","unit":"%","left_label":"fallan ATS","kicker":"Diagnóstico","headline":"3 de 4 CVs son rechazados automáticamente.","body":"Sin llegar a un humano."}}},
    {"slug":"slide-frame-within-frame","title":"Frame Within Frame","tier":"3_layout","system":"s05","cat":"Layout","desc":"Quote or content inside a nested decorative frame.",
     "showcase":{"layout":"slide-frame-within-frame",
        "copy":{"kicker":"Testimonio","quote":"Cambié el formato. No el contenido. Y empezaron a llamarme.","attribution":"María L · Product Manager · 2026"}}},
    {"slug":"slide-terminal-fullscreen","title":"Terminal Fullscreen","tier":"3_layout","system":"s29","cat":"Layout","desc":"Full-bleed terminal window with macOS chrome — cyberpunk.",
     "showcase":{"layout":"slide-terminal-fullscreen","layers":["geo-pixel-grid","scan-lines"],
        "copy":{"command":"ats-check --verbose cv.pdf","output_lines":[{"type":"ok","text":"Texto extraído: 487 palabras"},{"type":"warn","text":"Foto de perfil detectada — ignorada"},{"type":"err","text":"Tabla en Experiencia — parseo fallido"},{"type":"ok","text":"Keywords relevantes: 12/20"},{"type":"ok","text":"Score ATS: 61/100"}]}}},
    {"slug":"slide-editorial-column","title":"Editorial Column","tier":"3_layout","system":"s05","cat":"Layout","desc":"Single justified text column — magazine editorial format.",
     "showcase":{"layout":"slide-editorial-column",
        "copy":{"kicker":"Editorial","headline":"Por qué el formato importa más que el contenido.","body":"El ATS no lee. Extrae. Si el texto no está en orden lineal, desaparece antes de que un humano lo vea."}}},
    {"slug":"slide-badge-grid","title":"Badge Grid","tier":"3_layout","system":"s17","cat":"Layout","desc":"Grid of icon + label + description badges.",
     "showcase":{"layout":"slide-badge-grid",
        "copy":{"kicker":"Optimizado para","headline":"Todos los ATS del mercado.",
           "items":[{"icon":"target","title":"Workday","desc":"Más usado en US"},{"icon":"shield","title":"Taleo","desc":"Banca LATAM"},{"icon":"lightning","title":"Greenhouse","desc":"Startups tech"},{"icon":"chart","title":"Lever","desc":"Mid-market"},{"icon":"lock","title":"iCIMS","desc":"Retail + logística"},{"icon":"star","title":"SAP","desc":"Corporativo global"}]}}},
    {"slug":"slide-contrast-knockout","title":"Contrast Knockout","tier":"3_layout","system":"s07","cat":"Layout","desc":"High-contrast two-zone layout: dark top / light knockout bottom.",
     "showcase":{"layout":"slide-contrast-knockout",
        "copy":{"kicker":"Contraste","headline":"El ATS no sabe si sos bueno.","body":"Solo sabe si el texto coincide con las palabras clave del puesto."}}},
    {"slug":"slide-circular-quote","title":"Circular Quote","tier":"3_layout","system":"s04","cat":"Layout","desc":"Short quote centered inside a large circle.",
     "showcase":{"layout":"slide-circular-quote",
        "copy":{"kicker":"Resultado","quote":"Mandé 40 aplicaciones. Luego optimicé el CV. En la 41 conseguí entrevista.","attribution":"Juan D · Developer"}}},
    {"slug":"slide-waterfall-list","title":"Waterfall List","tier":"3_layout","system":"s17","cat":"Layout","desc":"Numbered items with cascading offset — waterfall flow.",
     "showcase":{"layout":"slide-waterfall-list",
        "copy":{"headline":"5 cambios que duplican tus entrevistas.",
           "items":[{"title":"Formato plano","desc":"Sin tablas, sin columnas."},{"title":"Keywords del puesto","desc":"Exactas, no sinónimos."},{"title":"Métricas en cada bullet","desc":"Números, no adjetivos."},{"title":"Resumen profesional","desc":"3 líneas, enfocado en el puesto."},{"title":"Sección Skills limpia","desc":"Lista plana, no tabla."}]}}},
    {"slug":"slide-angled-text","title":"Angled Text","tier":"3_layout","system":"s07","cat":"Layout","desc":"Rotated headline — dynamic editorial diagonal composition.",
     "showcase":{"layout":"slide-angled-text",
        "copy":{"kicker":"Rotación","headline":"Texto en\nángulo editorial.","body":"Eje diagonal para romper la horizontalidad del canvas."}}},
    {"slug":"slide-minimal-card-stack","title":"Minimal Card Stack","tier":"3_layout","system":"s05","cat":"Layout","desc":"Clean stacked cards with minimal border/shadow separation.",
     "showcase":{"layout":"slide-minimal-card-stack",
        "copy":{"headline":"Qué incluye el análisis.",
           "cards":[{"title":"Scan ATS completo","desc":"Score por sección + keywords faltantes."},{"title":"Reescritura de bullets","desc":"Resultados cuantificados en cada puesto."},{"title":"Optimización LinkedIn","desc":"Headline + About + Skills alineados."}]}}},
    {"slug":"slide-logo-wall","title":"Logo Wall","tier":"3_layout","system":"s05","cat":"Layout","desc":"Client logos or press mentions in a full grid.",
     "showcase":{"layout":"slide-logo-wall",
        "copy":{"headline":"ATS más comunes en LATAM",
           "logos":["Workday","Taleo","Greenhouse","Lever","iCIMS","SAP","BambooHR","Bullhorn","JazzHR","SmartRecruiters","Oracle","Zoho"]}}},
    {"slug":"slide-receipt","title":"Receipt","tier":"3_layout","system":"s17","cat":"Layout","desc":"Thermal receipt UI — itemized line-by-line breakdown.",
     "showcase":{"layout":"slide-receipt",
        "copy":{"headline":"REPORTE ATS ·····",
           "items":[{"label":"Formato","value":"PASS"},{"label":"Texto extraíble","value":"PASS"},{"label":"Sin tablas","value":"PASS"},{"label":"Keywords","value":"12/20"},{"label":"Foto","value":"FAIL"},{"label":"Score final","value":"61/100"}],"total":"OPTIMIZAR → 84+"}}},
    {"slug":"slide-polaroid-grid","title":"Polaroid Grid","tier":"3_layout","system":"s04","cat":"Layout","desc":"Polaroid-style photo cards with caption — testimonials.",
     "showcase":{"layout":"slide-polaroid-grid",
        "copy":{"kicker":"Prueba social","headline":"Resultados reales.",
           "cards":[{"color_gradient":"linear-gradient(135deg,var(--accent),rgba(0,0,0,0.4))","icon":"trophy","caption":"Carlos · QA · +4 entrevistas"},{"color_gradient":"linear-gradient(135deg,#ff7eb3,rgba(0,0,0,0.4))","icon":"star","caption":"María · PM · oferta en 3 semanas"},{"color_gradient":"linear-gradient(135deg,#4ecdc4,rgba(0,0,0,0.4))","icon":"chart","caption":"Luis · Data · +22% salario"}]}}},
    {"slug":"slide-tag-cloud","title":"Tag Cloud","tier":"3_layout","system":"s17","cat":"Layout","desc":"Keyword cloud with variable size + opacity scatter.",
     "showcase":{"layout":"slide-tag-cloud",
        "copy":{"kicker":"Keywords","headline":"Las 12 palabras que detecta el ATS.",
           "words":[{"text":"Python","size":"44px"},{"text":"SQL","size":"32px"},{"text":"Agile","size":"28px"},{"text":"AWS","size":"36px"},{"text":"Docker","size":"22px"},{"text":"Kubernetes","size":"26px"},{"text":"CI/CD","size":"30px"},{"text":"JIRA","size":"18px"},{"text":"Scrum","size":"34px"},{"text":"REST","size":"20px"},{"text":"PostgreSQL","size":"24px"},{"text":"Git","size":"40px"}]}}},
    {"slug":"slide-morse-code","title":"Morse Code","tier":"3_layout","system":"s29","cat":"Layout","desc":"Message encoded in Morse dots/dashes — cyberpunk only.",
     "showcase":{"layout":"slide-morse-code","layers":["geo-pixel-grid"],
        "copy":{"headline":"Mensaje en código.","message":"WORQAI","decoded_text":"Tu CV habla en un idioma que el ATS entiende."}}},
    {"slug":"slide-scroll-code","title":"Scroll Code","tier":"3_layout","system":"s29","cat":"Layout","desc":"Scrollable code snippet with syntax color — dev aesthetic.",
     "showcase":{"layout":"slide-scroll-code","layers":["geo-scan-lines"],
        "copy":{"language":"python","headline":"3 líneas de WorqAI.",
           "code_lines":["# Optimiza tu CV con IA","from worqai import CVOptimizer","","optimizer = CVOptimizer()","result = optimizer.analyze('cv.pdf')","print(result.score, result.keywords)","# Score: 84/100 · keywords: 18/20"]}}},
    {"slug":"slide-pull-quote","title":"Pull Quote","tier":"3_layout","system":"s05","cat":"Layout","desc":"Centered quote with large decorative quotation mark.",
     "showcase":{"layout":"slide-pull-quote",
        "copy":{"quote":"El problema no era mi experiencia. Era cómo la presentaba.","author_name":"Sofía R","author_role":"Product Manager · 2026","author_initial":"S"}}},
    {"slug":"slide-cross-slide-connector","title":"Cross-Slide Connector","tier":"3_layout","system":"s17","cat":"Layout","desc":"Visual anchor slide for multi-slide continuity flows.",
     "showcase":{"layout":"slide-cross-slide-connector",
        "copy":{"kicker":"Continuidad","headline":"Conector de flujo.","body":"Slide de transición entre secciones de un carousel."}}},
    {"slug":"slide-checklist","title":"Checklist","tier":"3_layout","system":"s17","cat":"Layout","desc":"Numbered checklist with problem label + fix per row.",
     "showcase":{"layout":"slide-checklist",
        "copy":{"kicker":"Lista","headline":"5 cosas a revisar antes de enviar.",
           "tips":[{"problem":"Tablas o columnas","fix":"Convertir a texto plano."},{"problem":"Foto de perfil","fix":"Eliminar — el ATS la ignora o bloquea."},{"problem":"Fuentes decorativas","fix":"Cambiar a Inter, Arial o Calibri."},{"problem":"Sin métricas","fix":"Agregar números a cada bullet."},{"problem":"Keywords genéricas","fix":"Usar exactamente las palabras del puesto."}]}}},
    {"slug":"slide-big-number","title":"Big Number","tier":"3_layout","system":"s17","cat":"Layout","desc":"Large centered stat with kicker and supporting body text.",
     "showcase":{"layout":"slide-big-number",
        "copy":{"kicker":"Dato clave","stat_number":"6x","stat_context":"más entrevistas con CV optimizado","headline":"El formato importa","body":"CVs ATS-optimizados obtienen 6 veces más respuestas."}}},
    {"slug":"slide-hook-lockup","title":"Hook Lockup","tier":"3_layout","system":"s17","cat":"Layout","desc":"Default hook slide. Kicker + headline + body + swipe prompt.",
     "showcase":{"layout":"slide-hook-lockup","layers":["glow-orb"],
        "copy":{"kicker":"ATS","headline":"El 94% de los CVs nunca los ve un humano.","body":"Los sistemas ATS filtran antes que cualquier reclutador. Así que tu CV tiene dos audiencias: un robot y una persona.","swipe_prompt":"Deslizá para ver cómo pasar el filtro"}}},
    {"slug":"slide-cta","title":"CTA Slide","tier":"3_layout","system":"s17","cat":"Layout","desc":"Question + keyword CTA + reward. Final slide default.",
     "showcase":{"layout":"slide-cta","layers":["zoom-rings"],
        "copy":{"question":"¿Querés que tu CV pase el ATS?","cta_keyword":"GRATIS","reward":"Optimización completa en 48hs. Garantía de paso ATS."}}},
    {"slug":"slide-terminal","title":"Terminal","tier":"3_layout","system":"s29","cat":"Layout","desc":"Mock terminal output. Diagnostic / shock slides.",
     "showcase":{"layout":"slide-terminal","layers":["pw-grid","scan-lines"],
        "copy":{"kicker":"Diagnóstico","headline":"Tu CV no está roto. Está en otro idioma.","command":"ats-check --file cv.pdf","output_lines":[{"type":"ok","text":"✓ Formato: PDF pasable"},{"type":"warn","text":"⚠ Columnas detectadas"},{"type":"err","text":"✗ Sin keywords de JD"},{"type":"info","text":"→ Score: 23/100"}]}}},
    {"slug":"slide-before-after","title":"Before/After Columns","tier":"3_layout","system":"s17","cat":"Layout","desc":"Column comparison. Coexists with stacked variant.",
     "showcase":{"layout":"slide-before-after","layers":["diag-band"],
        "copy":{"headline":"Antes vs. Después","before_items":["Columnas","Colores","Gráficos"],"after_items":["Texto plano","Keywords","Estructura lógica"],"before_score":"12%","after_score":"94%"}}},

    # ═══════════════════════════════════════════════════════════════════════
    # SUB-COMPONENTS (22)
    # ═══════════════════════════════════════════════════════════════════════
    {"slug":"sub-stamp-circle","title":"Stamp Circle","tier":"4_sub","system":"s17","cat":"Sub","desc":"Round badge: NUEVO/GRATIS/URGENTE.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Stamp","headline":"Badge para promos."},
        "extras":'<div class="sub-stamp-circle" style="position:absolute;top:64px;right:64px;z-index:9">GRATIS</div>'}},
    {"slug":"sub-pill-tag","title":"Pill Tag","tier":"4_sub","system":"s17","cat":"Sub","desc":"Small accent category pill.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Tags","headline":"Pills inline","body":"<span class=\'sub-pill-tag\'>ATS</span> <span class=\'sub-pill-tag solid\'>LATAM</span> <span class=\'sub-pill-tag\'>Tech</span>"}}},
    {"slug":"sub-arrow-flow","title":"Arrow Flow","tier":"4_sub","system":"s17","cat":"Sub","desc":"Directional arrow between steps.",
     "showcase":{"layout":"slide-step-flow","copy":{"kicker":"Arrows","headline":"Conector entre pasos.",
        "steps":[{"title":"Antes","desc":"Score 12"},{"title":"Rewrite","desc":"Optimización"},{"title":"Después","desc":"Score 84"}]}}},
    {"slug":"sub-icon-circle","title":"Icon Circle","tier":"4_sub","system":"s17","cat":"Sub","desc":"Circular icon container.",
     "showcase":{"layout":"slide-icon-grid","copy":{"kicker":"Icons","headline":"Contenedor circular.",
        "tiles":[{"icon":"A","title":"Acción","desc":"Solid + outline."},{"icon":"B","title":"Beneficio","desc":"Reutilizable."},{"icon":"C","title":"Categoría","desc":"24-48px."}]}}},
    {"slug":"sub-dotted-divider","title":"Dotted Divider","tier":"4_sub","system":"s05","cat":"Sub","desc":"Horizontal dotted separator.",
     "showcase":{"layout":"slide-pull-quote-author","copy":{"kicker":"Editorial","quote":"Pausa visual sin línea sólida.","author":"Divider Note","role":"Spacing"}}},
    {"slug":"sub-rating-stars","title":"Rating Stars","tier":"4_sub","system":"s17","cat":"Sub","desc":"5-star rating row.",
     "showcase":{"layout":"slide-pull-quote-author","copy":{"kicker":"5 estrellas","quote":"Servicio brutal. Cambió mi proceso.","author":"María L","role":"Senior PM"}}},
    {"slug":"sub-logo-row","title":"Logo Row","tier":"4_sub","system":"s17","cat":"Sub","desc":"'As seen in' press logo row.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Press","headline":"Como visto en.","body":"<div class=\'sub-logo-row\' style=\'margin-top:16px\'><span class=\'logo\'>FORBES</span><span class=\'logo\'>WIRED</span><span class=\'logo\'>TC</span></div>"}}},
    {"slug":"sub-avatar-stack","title":"Avatar Stack","tier":"4_sub","system":"s17","cat":"Sub","desc":"Overlapping circular avatars.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Social proof","headline":"+2,847 latinos","body":"<div class=\'sub-avatar-stack\' style=\'margin-top:14px\'><span class=\'av\'>C</span><span class=\'av\'>M</span><span class=\'av\'>S</span><span class=\'av\'>L</span><span class=\'av more\'>+99</span></div>"}}},
    {"slug":"sub-fact-bubble","title":"Fact Bubble","tier":"4_sub","system":"s17","cat":"Sub","desc":"Speech bubble for myth vs fact.",
     "showcase":{"layout":"slide-myth-vs-fact","copy":{"kicker":"Bubble","headline":"Myth + fact pattern.",
        "myth":"Mandar 100 aplicaciones aumenta tus chances.","fact":"3 aplicaciones segmentadas convierten más que 100 spam."}}},
    {"slug":"sub-timeline-dot","title":"Timeline Dot","tier":"4_sub","system":"s17","cat":"Sub","desc":"Connector dot for timeline.",
     "showcase":{"layout":"slide-timeline","copy":{"kicker":"Dots","headline":"Conector usado en timeline.",
        "events":[{"date":"Día 1","title":"Inicio","desc":"Dot demo."},{"date":"Día 14","title":"Medio","desc":"Dot demo."},{"date":"Día 30","title":"Final","desc":"Dot demo."}]}}},
    {"slug":"sub-bento-card","title":"Bento Card","tier":"4_sub","system":"s17","cat":"Sub","desc":"Base card for bento grid.",
     "showcase":{"layout":"slide-bento-grid","copy":{"kicker":"Card","headline":"Tarjeta base reutilizable.","grid":"g-2x2",
        "tiles":[{"label":"Standard","title":"Card","body":"Background sutil + borde."},{"label":"Accent","title":"Card","body":"Color accent.","accent":True},{"label":"Standard","title":"Card","body":"Tercera."},{"label":"Standard","title":"Card","body":"Cuarta."}]}}},
    {"slug":"sub-inline-stat","title":"Inline Stat","tier":"4_sub","system":"s17","cat":"Sub","desc":"Large accent stat embedded inline.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Inline","headline":"Hasta <span class=\'sub-inline-stat\'>4x</span> entrevistas.","body":"Stat dentro del flow del texto."}}},
    {"slug":"sub-status-pill","title":"Status Pill","tier":"4_sub","system":"s17","cat":"Sub","desc":"Pass/fail/warn colored pill.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Status","headline":"Pills de estado.","body":"<span class=\'sub-status-pill pass\'>PASS</span> &nbsp; <span class=\'sub-status-pill warn\'>WARN</span> &nbsp; <span class=\'sub-status-pill fail\'>FAIL</span>"}}},
    {"slug":"sub-comment-mock","title":"Comment Mock","tier":"4_sub","system":"s17","cat":"Sub","desc":"Fake IG/LinkedIn comment.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Social","headline":"Comentario fake.",
        "body":"<div class=\'sub-comment-mock\'><div class=\'com-av\'>S</div><div class=\'com-body\'><div class=\'com-handle\'>@sofia.r · 2h</div><div class=\'com-text\'>Esto me cambió cómo veo mi CV. Gracias.</div></div></div>"}}},
    {"slug":"sub-handle-line","title":"Handle Line","tier":"4_sub","system":"s17","cat":"Sub","desc":"@user · 2h attribution line.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Handle","headline":"Atribución IG-style.","body":"<div class=\'sub-handle-line\'><span class=\'handle\'>@carlos.qa</span><span class=\'dot\'>·</span>2h<span class=\'dot\'>·</span>Senior QA</div>"}}},
    {"slug":"sub-stat-card","title":"Stat Card","tier":"4_sub","system":"s17","cat":"Sub","desc":"Base card for stat-row layout.",
     "showcase":{"layout":"slide-stat-row","copy":{"kicker":"Stat card","headline":"Base reutilizable.",
        "stats":[{"num":"01","label":"Demo card","body":"Reutilizable horizontal."},{"num":"02","label":"Demo card","body":"Misma estructura."},{"num":"03","label":"Demo card","body":"Variantes vía clase."}]}}},
    {"slug":"sub-chip-list","title":"Chip List","tier":"4_sub","system":"s17","cat":"Sub","desc":"Small chip/tag list.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Chips","headline":"Lista de keywords.","body":"<div class=\'sub-chip-list\' style=\'margin-top:18px\'><span class=\'chip\'>Python</span><span class=\'chip\'>AWS</span><span class=\'chip\'>Kubernetes</span><span class=\'chip\'>SQL</span><span class=\'chip\'>Docker</span></div>"}}},
    {"slug":"sub-download-card","title":"Download Card","tier":"4_sub","system":"s17","cat":"Sub","desc":"File icon + download CTA.",
     "showcase":{"layout":"slide-cta","copy":{"question":"Descargá la plantilla.","cta_keyword":"PDF","reward":"Plantilla ATS gratis — directo a tu email."}}},
    {"slug":"sub-emoji-callout","title":"Emoji Callout","tier":"4_sub","system":"s04","cat":"Sub","desc":"Single large emoji + caption.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Callout","headline":"Emoji + caption.","body":"<div class=\'sub-emoji-callout\' style=\'margin-top:24px\'><div class=\'ec-emoji\'>📄</div><div class=\'ec-text\'>Tu CV es el primer impreso.</div></div>"}}},
    {"slug":"sub-swipe-arrow-stack","title":"Swipe Arrow Stack","tier":"4_sub","system":"s17","cat":"Sub","desc":"Vertical chevron stack alt to swipe-pill.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Swipe","headline":"Stack vertical de chevrons.","body":"Reemplazo discreto del swipe-pill."},
        "extras":'<div class="sub-swipe-arrow-stack"><span>›</span><span>›</span><span>›</span></div>'}},
    {"slug":"glass-panel","title":"Glassmorphism Panel","tier":"4_sub","system":"s17","cat":"Sub","desc":"Frosted glass with backdrop-filter. PLAYWRIGHT recommended.",
     "showcase":{"layout":"slide-hook-lockup","copy":{"kicker":"Depth","headline":"Panel de cristal.","body":"backdrop-filter + gradient fallback para html2canvas."},
        "extras":'<div class="glass-panel" style="position:absolute;top:64px;right:64px;width:200px;height:120px;z-index:9;display:flex;align-items:center;justify-content:center;font-family:var(--font-mono);font-size:10px;letter-spacing:0.14em;text-transform:uppercase;color:var(--accent);opacity:0.8">Glass</div>'}},
    {"slug":"watermark","title":"Watermark","tier":"4_sub","system":"s17","cat":"Sub","desc":"Giant faint letter/symbol behind content.",
     "showcase":{"layout":"slide-big-number","layers":["geo-halftone"],
        "decoratives":["watermark"],
        "copy":{"kicker":"Watermark","stat_number":"W","stat_context":"marca fantasma","headline":"Sello sutil"}}},

    # ═══════════════════════════════════════════════════════════════════════
    # CSS TECHNIQUES (3)
    # ═══════════════════════════════════════════════════════════════════════
    {"slug":"css-text-gradient","title":"Text Gradient","tier":"5_css","system":"s01","cat":"CSS","desc":"SVG linearGradient text fill. Accent to white.",
     "showcase":{"layout":"slide-big-number","copy":{"kicker":"CSS","stat_number":"84%","stat_context":"gradient fill","text_treatment":"gradient","headline":"Gradient text","body":"SVG linearGradient desde accent a blanco."}}},
    {"slug":"css-text-glow","title":"Text Glow","tier":"5_css","system":"s29","cat":"CSS","desc":"Multi-layer neon text-shadow glow.",
     "showcase":{"layout":"slide-big-number","copy":{"kicker":"CSS","stat_number":"Glow","stat_context":"neon shadow","text_treatment":"glow","headline":"Neon glow","body":"3 capas de text-shadow para efecto tubo."}}},
    {"slug":"css-text-stroke","title":"Text Stroke","tier":"5_css","system":"s07","cat":"CSS","desc":"Outline stroke with transparent fill.",
     "showcase":{"layout":"slide-big-number","copy":{"kicker":"CSS","stat_number":"OUT","stat_context":"stroke only","text_treatment":"stroke","headline":"Stroke text","body":"-webkit-text-stroke con fill transparente."}}},
]

# ─── Auto-generate AI Background demos from manifest ──────────────────────────
def _load_ai_bg_manifest() -> list:
    manifest_path = ROOT / "brand" / "generated-bg" / "manifest.json"
    if not manifest_path.exists():
        return []
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        return data.get("backgrounds", [])
    except Exception:
        return []


_AI_BGS = _load_ai_bg_manifest()
for bg in _AI_BGS:
    bg_id = bg["id"]
    bg_name = bg["name"]
    # Use s17 (lime) as the default showcase system since it's the brand
    showcase_system = "s17"
    DEMOS.append({
        "slug": bg_id,
        "title": bg_name,
        "tier": "1_geo",
        "system": showcase_system,
        "cat": "AI-BG",
        "desc": f"AI-generated background image, color-adapted to visual systems.",
        "showcase": {
            "layout": "slide-hook-lockup",
            "layers": [bg_id],
            "copy": {
                "kicker": "AI GENERADO",
                "headline": "Fondos generados\\npor inteligencia artificial.",
                "body": "Imagen adaptada automaticamente al sistema visual.",
            },
        },
    })

# ─── Validation ───────────────────────────────────────────────────────────────
assert len(DEMOS) == 122 + len(_AI_BGS), f"Expected {122 + len(_AI_BGS)} demos, got {len(DEMOS)}"

# ─── Visual Systems metadata ──────────────────────────────────────────────────
SYSTEM_NAMES = {
    "s01":"NOIR GOLD","s02":"ROYAL BLUE","s03":"DEEP FOREST","s04":"CRIMSON NIGHT",
    "s05":"STARK WHITE","s06":"AURORA","s07":"BRUTALIST","s08":"GLASSMORPHISM",
    "s09":"CHROME SILVER","s10":"TERRA COTTA","s11":"TROPIC","s12":"WARM SAND",
    "s13":"OBSIDIAN ROSE","s14":"DEEP SEA","s15":"OXFORD NIGHT","s16":"NEON GRID",
    "s17":"WORQAI VERDE","s18":"RISO LAB","s19":"SWISS GRID","s20":"Y2K CHROME",
    "s21":"VAPOR GRIDWAVE","s22":"DARK ACADEMIA","s23":"QUIET LUXURY","s24":"HARAJUKU POP",
    "s25":"SWISS BRUT","s26":"MATTE PASTEL","s27":"NEO RISO","s28":"MONO CONTRAST",
    "s29":"CYBERPUNK","s30":"ANALOG LO-FI","s31":"NEOBRUT","s32":"MAXIMALIST",
    "s33":"CLEAN SAAS","s34":"PANTONE EDI","s35":"ART DECO","s36":"MEXICAN MOD",
    "s37":"AFROFUTURIST","s38":"LATAM MURAL","s39":"MINIMAL JPN","s40":"GLITCH",
    "s41":"HOLOGRAPHIC","s42":"ARCHITECTURAL","s43":"GEN Z POP","s44":"CHALKBOARD",
    "s45":"RISO BLUE-RED","s46":"BLUEPRINT","s47":"STONE LIBRARY","s48":"BOUTIQUE EDI",
}

# Slugs that were added in the most recent expansion (badge as NEW)
NEW_SLUGS = {
    "geo-blob-bg","geo-glow-orb","geo-zoom-rings","geo-grid-bg","geo-diag-band",
    "slide-proof","slide-tip-blocks","slide-massive-number","slide-full-bleed-type",
    "slide-diagonal-split","slide-asymmetric-lockup","slide-type-over-shape",
    "slide-stacked-type","slide-corner-manifesto","slide-data-wall","slide-side-by-side",
    "slide-frame-within-frame","slide-terminal-fullscreen","slide-editorial-column",
    "slide-badge-grid","slide-contrast-knockout","slide-circular-quote",
    "slide-waterfall-list","slide-angled-text","slide-minimal-card-stack",
    "slide-logo-wall","slide-receipt","slide-polaroid-grid","slide-tag-cloud",
    "slide-morse-code","slide-scroll-code","slide-pull-quote","slide-cross-slide-connector",
    "slide-checklist","slide-big-number","slide-hook-lockup","slide-cta",
    "slide-terminal","slide-before-after","pw-grid","vol-light","svg-blob-tr",
    "svg-blob-bl","svg-blob-center","svg-blob-asymmetric","svg-blob-scattered",
    "svg-blob-angular","svg-blob-crystal","svg-blob-wave","svg-blob-arch",
    "svg-blob-splatter","svg-blob-ribbon","geo-flow-wave","geo-flow-arrow",
    "geo-flow-data","watermark","css-text-gradient","css-text-glow","css-text-stroke",
}

# ─── Spec builders ────────────────────────────────────────────────────────────

def make_spec_context(demo: dict) -> dict:
    """Build a 1-slide spec — in-context view with original system and copy."""
    showcase = demo["showcase"]
    slide = {
        "id": "s1",
        "layout": showcase["layout"],
        "copy": showcase.get("copy", {}),
    }
    if "layers" in showcase:
        slide["layers"] = showcase["layers"]
    if "extras" in showcase:
        slide["__extras"] = showcase["extras"]
    if "decoratives" in showcase:
        slide["decoratives"] = showcase["decoratives"]
    return {
        "meta": {
            "system": demo["system"],
            "aspect": "1:1",
            "slides": 1,
            "brand": "@worqai",
            "language": "es-LATAM",
            "topic": demo["slug"],
        },
        "pacing": ["data"],
        "slides": [slide],
    }


def make_spec_component(demo: dict) -> dict:
    """Build a 1-slide spec — isolated view on dark s01 bg with minimal copy."""
    showcase = demo["showcase"]
    slide = {
        "id": "s1",
        "layout": showcase["layout"],
        "copy": {},
    }

    # Preserve essential structural fields so the layout/component renders
    essential = [
        "output_lines","command","code_lines","language","percent","center_label",
        "filled","label","before_items","after_items","before_score","after_score",
        "before_label","after_label","before_text","after_text","before_pct","after_pct",
        "myth","fact","steps","events","stats","bars","items","tips","faqs","quotes",
        "tiles","quote","author","role","attribution","logos","words","cards","rows",
        "headers","grid","stat_number","unit","left_content","left_label","left_number",
        "input_label","input_text","output_label","output_text","message","decoded_text",
        "icon","eyebrow","footer_left","footer_right","lines","stat_context","context",
        "source","question","cta_keyword","reward","url","text_treatment",
    ]
    sc = showcase.get("copy", {})
    for field in essential:
        if field in sc:
            slide["copy"][field] = sc[field]

    # Minimal kicker with component name
    slide["copy"]["kicker"] = demo["title"].upper()

    if "layers" in showcase:
        slide["layers"] = showcase["layers"]
    if "decoratives" in showcase:
        slide["decoratives"] = showcase["decoratives"]

    # Inject bottom label as extras (merged with any existing extras)
    label_html = (
        f'<div class="comp-label" style="position:absolute;bottom:10px;left:0;right:0;'
        f'text-align:center;font-family:\'JetBrains Mono\',monospace;'
        f'font-size:9px;letter-spacing:0.12em;text-transform:uppercase;'
        f'color:rgba(255,255,255,0.35);z-index:50">{demo["title"]}</div>'
    )
    existing = showcase.get("extras", "")
    slide["__extras"] = existing + "\n  " + label_html if existing else label_html

    return {
        "meta": {
            "system": "s01",
            "aspect": "1:1",
            "slides": 1,
            "brand": "@worqai",
            "language": "es-LATAM",
            "topic": demo["slug"],
        },
        "pacing": ["data"],
        "slides": [slide],
    }


def inject_extras(html: str, extras_html: str) -> str:
    """Inject raw HTML extras into the first slide div."""
    if not extras_html:
        return html
    parts = html.split('<div class="slide')
    if len(parts) >= 2:
        slide_body = parts[1]
        gt = slide_body.find('>')
        if gt > 0:
            slide_body = slide_body[:gt+1] + "\n  " + extras_html + "\n" + slide_body[gt+1:]
            parts[1] = slide_body
            return '<div class="slide'.join(parts)
    return html


def isolate_html(html: str, demo: dict) -> str:
    """Strip a rendered carousel down to component-only for isolated gallery view."""
    cat = demo["cat"]

    # ── Base: hide preview chrome, make full-screen ──
    css = """
/* === ISOLATION === */
.label-top { display: none !important; }
.preview-cage, .viewer, .wrap, .track {
  width: 100% !important; height: 100% !important;
  max-width: none !important; border-radius: 0 !important;
  box-shadow: none !important; overflow: visible !important;
}
.slide { min-width: 100% !important; }
.brand, .counter, .prog, .swipe-pill { display: none !important; }
.deco-corner-tl, .deco-corner-br, .deco-watermark,
.deco-starburst, .deco-starburst-tr, .deco-starburst-spark,
.deco-starburst-burst, .deco-starburst-mark,
.chrome-vertical-counter, .chrome-badge-stamp, .chrome-header-bar { display: none !important; }
"""

    # ── Hide all geo layers ──
    css += """
.pw-wrap, .pw-grid, .glow-orb, .vol-light, .blob-bg, .grid-bg, .diag-band,
.zoom-rings, .scan-lines,
.geo-mesh-noise, .geo-pixel-grid, .geo-conic-rays, .geo-chevron-stripe,
.geo-iso-grid, .geo-paper-texture, .geo-halftone, .geo-ribbon-flow,
.geo-circuit-trace, .geo-topo-lines, .geo-starfield, .geo-gradient-bands,
.geo-contour-flow, .geo-perspective-grid, .geo-hex-mesh, .geo-constellation,
.geo-neon-ring, .geo-bokeh, .geo-scan-lines, .geo-chromatic-edge,
.geo-data-streaks, .geo-liquid-morph, .geo-flow-wave, .geo-flow-arrow,
.geo-flow-data,
.svg-blob-tr, .svg-blob-bl, .svg-blob-center, .svg-blob-asymmetric,
.svg-blob-scattered, .svg-blob-angular, .svg-blob-crystal, .svg-blob-wave,
.svg-blob-arch, .svg-blob-splatter, .svg-blob-ribbon,
.continuity-wave, .continuity-arrow, .continuity-pipeline { display: none !important; }
"""

    ALL_LAYOUT_WRAPPERS = """.hook-wrap, .stat-wrap, .term-wrap, .tip-wrap, .ba-wrap, .chk-wrap,
.proof-wrap, .cta-wrap, .quote-wrap, .step-wrap, .bento-wrap, .grid-wrap,
.compare-wrap, .comp-table-wrap, .faq-wrap, .timeline-wrap, .warn-wrap,
.poster-wrap, .mvf-wrap, .cascade-wrap, .statrow-wrap, .qauth-wrap,
.pbar-wrap, .lnum-wrap, .donut-wrap, .fbt-wrap, .diags-wrap, .asym-wrap,
.tos-wrap, .stype-wrap, .cman-wrap, .dwall-wrap, .sbs-wrap, .fwf-wrap,
.mn-wrap, .tfs-wrap, .ec-wrap, .badgeg-wrap, .ck-wrap, .cq-wrap, .wfl-wrap,
.at-wrap, .mcs-wrap, .lw-wrap, .rcpt-wrap, .pg-wrap, .tc-wrap, .mc-wrap,
.sc-wrap, .io-wrap, .waffle-wrap, .bas-wrap, .conn-wrap, .icong-wrap { display: none !important; }"""

    if cat == "Geo":
        # Hide all layout wrappers — show only the specific geo layer(s)
        css += "\n" + ALL_LAYOUT_WRAPPERS
        layers = demo.get("showcase", {}).get("layers", [])
        for layer in layers:
            css += f"\n.{layer} {{ display: block !important; }}"
            if layer == "pw-grid":
                css += "\n.pw-wrap { display: block !important; }"
        css += "\n.slide { padding: 0 !important; }"

    elif cat == "Layout":
        # Layout IS the component — keep layout wrapper visible, only hide geo/chrome
        css += "\n.slide { padding-bottom: var(--pad-y) !important; }"

    elif cat in ("Sub", "Chrome"):
        # Sub-component IS the feature — show full layout so component is visible in context
        css += "\n.slide { padding-bottom: var(--pad-y) !important; }"

    elif cat == "CSS":
        # Show layout with text treatment, hide geo/chrome decoratives
        css += "\n.slide { padding-bottom: var(--pad-y) !important; }"

    elif cat == "AI-BG":
        # Show only the AI background image + overlay, hide layout text
        css += "\n" + ALL_LAYOUT_WRAPPERS
        css += "\n.geo-ai-bg { display: block !important; }"
        css += "\n.geo-ai-bg-overlay { display: block !important; }"
        css += "\n.slide { padding: 0 !important; }"

    # Inject before the closing </style> tag
    html = html.replace("</style>", css + "\n</style>", 1)
    return html


# ─── INDEX builder ────────────────────────────────────────────────────────────

def build_index(demos: list, systems_list: list = None) -> str:
    """Build gallery/INDEX.html — premium two-panel layout with toggle."""
    systems_list = systems_list or []
    sys_n = len(systems_list)

    cat_counts = {}
    for d in demos:
        cat_counts[d["cat"]] = cat_counts.get(d["cat"], 0) + 1

    total_n  = len(demos)
    geo_n    = cat_counts.get("Geo", 0)
    chrome_n = cat_counts.get("Chrome", 0)
    layout_n = cat_counts.get("Layout", 0)
    sub_n    = cat_counts.get("Sub", 0)
    css_n    = cat_counts.get("CSS", 0)
    ai_n     = cat_counts.get("AI-BG", 0)

    cat_color = {
        "Geo":    "#C7FF3A",
        "Chrome": "#feca57",
        "Layout": "#ff7eb3",
        "Sub":    "#4ecdc4",
        "CSS":    "#a855f7",
        "AI-BG":  "#00f0ff",
    }

    cards_html = []
    for i, d in enumerate(demos, 1):
        n = f"{i:02d}"
        col = cat_color.get(d["cat"], "#888")
        is_new = d["slug"] in NEW_SLUGS
        new_badge = '<span class="badge-new">NEW</span>' if is_new else ''
        cards_html.append(f'''
      <div class="card" data-cat="{d['cat']}" data-slug="{d['slug']}"
           data-component="{n}-{d['slug']}-component.html"
           data-context="{n}-{d['slug']}-context.html">
        <span class="card-num">{n}</span>
        <span class="card-body">
          <span class="card-cat" style="color:{col}">{d['cat']}</span>
          <span class="card-title">{d['title']}</span>
          <span class="card-desc">{d['desc']}</span>
        </span>
        <span class="card-toggle">
          <button class="ct-btn active" data-mode="component" title="Isolated">ISO</button>
          <button class="ct-btn" data-mode="context" title="In Slide">CTX</button>
        </span>
        {new_badge}
      </div>''')

    cards_joined = "\n".join(cards_html)

    # Build system preview cards
    syscards_html = []
    for s in systems_list:
        syscards_html.append(f'''
      <div class="scard" data-cat="Systems" data-slug="{s['sid']}" data-src="sys-{s['sid']}.html">
        <div class="scard-dots">
          <div class="scard-dot" style="background:{s['accent']}" title="Accent: {s['accent']}"></div>
          <div class="scard-dot scard-dot-bg" style="background:{s['bg']}" title="Base: {s['bg']}"></div>
        </div>
        <div class="scard-info">
          <span class="scard-id">{s['sid'].upper()}</span>
          <span class="scard-name">{s['name']}</span>
          <span class="scard-fonts">{s['font_display']} / {s['font_body']}</span>
        </div>
      </div>''')
    syscards_joined = "\n".join(syscards_html)

    # Use a template with ___PLACEHOLDERS___ to avoid f-string escaping hell
    template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>WorqAI · Component Gallery · ___TOTAL___</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&family=JetBrains+Mono:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden}
:root{
  --accent:#C7FF3A;
  --accent-dim:rgba(199,255,58,0.12);
  --bg:#080c0e;
  --panel:#0b0f14;
  --border:#111820;
  --border-light:#1a2332;
  --text:#c9d1d9;
  --text-dim:#8a9bb0;
  --text-faint:#3a4a5a;
  --text-dark:#1e2d3d;
}
body{
  font-family:'Inter',sans-serif;
  background:var(--bg);
  color:var(--text);
  display:grid;
  grid-template-rows:auto auto 1fr;
  grid-template-columns:minmax(300px,40%) 1fr;
}

/* ── Header ─────────────────────────────────────────────────────────── */
header{
  grid-column:1/-1;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 20px;height:56px;
  background:#0d1117;
  border-bottom:1px solid var(--border-light);
}
.logo{
  font-family:'JetBrains Mono',monospace;
  font-size:15px;font-weight:700;letter-spacing:0.14em;
  color:var(--accent);
  text-shadow:0 0 18px rgba(199,255,58,0.45),0 0 40px rgba(199,255,58,0.15);
}
.logo-sep{color:#2d4a6a;margin:0 8px}
.logo-sub{color:#4a5568;font-weight:400;font-size:12px;letter-spacing:0.08em}
.header-stats{
  display:flex;gap:20px;
  font-family:'JetBrains Mono',monospace;font-size:10px;color:#2d4a6a;
  letter-spacing:0.06em;
}
.hs-item span{color:var(--accent)}
.hs-sep{color:var(--border-light)}

/* ── Filter bar ─────────────────────────────────────────────────────── */
.filter-bar{
  grid-column:1/-1;
  display:flex;align-items:center;gap:6px;padding:0 14px;height:44px;
  background:var(--panel);border-bottom:1px solid var(--border);
}
.filter-btn{
  font-family:'JetBrains Mono',monospace;font-size:9px;font-weight:500;
  letter-spacing:0.12em;text-transform:uppercase;
  padding:4px 12px;background:transparent;
  border:1px solid var(--border-light);color:var(--text-faint);cursor:pointer;
  border-radius:3px;
}
.filter-btn:hover{border-color:#2d4a6a;color:#6a8aaa}
.filter-btn.on{background:var(--accent);color:var(--bg);border-color:var(--accent);font-weight:700}
.filter-sep{width:1px;height:20px;background:var(--border-light);margin:0 4px}
.filter-count{
  font-family:'JetBrains Mono',monospace;font-size:9px;color:#2d4a6a;
  letter-spacing:0.06em;margin-left:auto;
}
.filter-count span{color:#4a6a8a}

/* ── Nav panel ──────────────────────────────────────────────────────── */
nav{
  overflow-y:auto;
  background:var(--panel);
  border-right:1px solid var(--border);
  scrollbar-width:thin;
  scrollbar-color:var(--border-light) transparent;
  padding-bottom:20px;
}
nav::-webkit-scrollbar{width:3px}
nav::-webkit-scrollbar-track{background:transparent}
nav::-webkit-scrollbar-thumb{background:var(--border-light);border-radius:1px}

/* ── Cards ──────────────────────────────────────────────────────────── */
.card{
  display:grid;grid-template-columns:36px 1fr auto;
  gap:0 10px;align-items:start;
  padding:11px 14px;
  border-bottom:1px solid #0f141a;
  color:var(--text-dim);
  
  cursor:pointer;position:relative;
}
.card:hover{background:#0f141a;color:var(--text);border-left:2px solid var(--accent);padding-left:12px}
.card.active{
  background:#0f1a24;
  border-left:2px solid var(--accent);
  padding-left:12px;
  color:#e0e8f0;
}
.card-num{
  font-family:'JetBrains Mono',monospace;
  font-size:9px;color:var(--text-dark);letter-spacing:0.04em;
  padding-top:1px;
}
.card:hover .card-num,.card.active .card-num{color:#4a6a4a}
.card-body{display:flex;flex-direction:column;gap:2px;min-width:0}
.card-cat{
  font-family:'JetBrains Mono',monospace;
  font-size:8px;letter-spacing:0.16em;text-transform:uppercase;font-weight:700;
}
.card-title{font-size:12px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card-desc{font-size:10px;color:var(--text-faint);line-height:1.35;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card:hover .card-desc{color:#4a6a7a}

/* Card toggle (Component / Context) */
.card-toggle{
  display:flex;flex-direction:column;gap:2px;align-self:start;margin-top:1px;
}
.ct-btn{
  font-family:'JetBrains Mono',monospace;font-size:7px;font-weight:600;
  letter-spacing:0.06em;text-transform:uppercase;
  padding:2px 5px;background:transparent;border:1px solid var(--border-light);
  color:var(--text-faint);cursor:pointer;border-radius:2px;
  line-height:1;
}
.ct-btn:hover{border-color:#2d4a6a;color:#6a8aaa}
.ct-btn.active{background:var(--accent-dim);border-color:rgba(199,255,58,0.35);color:var(--accent)}

.badge-new{
  font-family:'JetBrains Mono',monospace;font-size:7px;font-weight:700;
  padding:2px 5px;letter-spacing:0.1em;text-transform:uppercase;
  background:var(--accent-dim);border:1px solid rgba(199,255,58,0.35);
  color:var(--accent);border-radius:2px;white-space:nowrap;
  position:absolute;top:11px;right:11px;
}

/* ── Preview panel ──────────────────────────────────────────────────── */
main{
  display:flex;flex-direction:column;
  background:#060a0c;
  overflow:hidden;
}
.preview-topbar{
  display:flex;align-items:center;justify-content:space-between;
  padding:0 14px;height:36px;
  background:var(--panel);border-bottom:1px solid var(--border);
  flex-shrink:0;
}
.preview-path{
  font-family:'JetBrains Mono',monospace;font-size:9px;color:#2d4a6a;
  letter-spacing:0.08em;
}
.preview-path span{color:#4a8a6a}
.preview-actions{display:flex;gap:6px}
.preview-btn{
  font-family:'JetBrains Mono',monospace;font-size:8px;letter-spacing:0.1em;
  text-transform:uppercase;padding:3px 8px;
  background:transparent;border:1px solid var(--border-light);color:#2d4a6a;cursor:pointer;
  text-decoration:none;border-radius:2px;
}
.preview-btn:hover{border-color:var(--accent);color:var(--accent)}
.preview-frame{
  flex:1;display:flex;align-items:center;justify-content:center;
  padding:20px;overflow:hidden;position:relative;
}
iframe{
  width:100%;
  max-width:min(calc(100vh - 160px), calc(100% - 40px));
  aspect-ratio:1/1;
  border:1px solid var(--border-light);
  background:#0a0a12;
  display:none;
  
}
.empty{
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  width:100%;height:100%;gap:16px;
  font-family:'JetBrains Mono',monospace;color:var(--text-dark);
}
.empty-prompt{
  font-size:11px;letter-spacing:0.1em;text-transform:uppercase;
}
.empty-sub{font-size:9px;color:#141c24;letter-spacing:0.06em;margin-top:4px}
.cursor{
  display:inline-block;width:8px;height:14px;background:var(--accent);
  opacity:0.7;vertical-align:middle;
}

/* ── System cards ───────────────────────────────────────────────────── */
.scard{
  display:grid;grid-template-columns:28px 1fr;
  gap:0 10px;align-items:center;
  padding:9px 14px;
  border-bottom:1px solid #0f141a;
  cursor:pointer;
}
.scard:hover{background:#0f141a;border-left:2px solid var(--accent);padding-left:12px}
.scard.active{background:#0f1a24;border-left:2px solid var(--accent);padding-left:12px}
.scard-dots{display:flex;flex-direction:column;gap:3px;align-items:flex-start}
.scard-dot{width:18px;height:18px;border-radius:4px;flex-shrink:0}
.scard-dot-bg{border:1px solid rgba(255,255,255,0.15)!important}
.scard-info{display:flex;flex-direction:column;gap:1px;min-width:0}
.scard-id{
  font-family:'JetBrains Mono',monospace;font-size:8px;
  letter-spacing:0.18em;color:#2d4a6a;text-transform:uppercase;
}
.scard:hover .scard-id,.scard.active .scard-id{color:#4a7a4a}
.scard-name{
  font-size:11px;font-weight:700;letter-spacing:0.06em;
  color:var(--text-dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.scard:hover .scard-name,.scard.active .scard-name{color:var(--text)}
.scard-fonts{
  font-size:9px;color:var(--text-faint);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}
.sys-section-header{
  padding:10px 14px 4px;
  font-family:'JetBrains Mono',monospace;font-size:8px;
  letter-spacing:0.18em;text-transform:uppercase;
  color:#2d4a6a;border-bottom:1px solid #0f141a;
}

/* ── Mobile ─────────────────────────────────────────────────────────── */
@media(max-width:768px){
  html,body{height:auto;overflow:auto}
  body{grid-template-rows:auto auto 50vh auto;grid-template-columns:1fr}
  main{order:-1;height:50vh}
  nav{max-height:none}
  iframe{max-width:100%}
}
</style>
</head>
<body>

<header>
  <div class="logo">
    WORQAI<span class="logo-sep">·</span><span class="logo-sub">Component Gallery</span>
  </div>
  <div class="header-stats">
    <span class="hs-item"><span>___TOTAL___</span> components</span>
    <span class="hs-sep">|</span>
    <span class="hs-item"><span>___GEO___</span> Geo</span>
    <span class="hs-item"><span>___CHROME___</span> Chrome</span>
    <span class="hs-item"><span>___LAYOUT___</span> Layout</span>
    <span class="hs-item"><span>___SUB___</span> Sub</span>
    <span class="hs-item"><span>___CSS___</span> CSS</span>
    <span class="hs-item"><span>___AI___</span> AI-BG</span>
    <span class="hs-sep">|</span>
    <span class="hs-item"><span>___SYS___</span> Systems</span>
  </div>
</header>

<div class="filter-bar" id="filter-bar">
  <button class="filter-btn on" data-cat="all">All</button>
  <button class="filter-btn" data-cat="Geo">Geo</button>
  <button class="filter-btn" data-cat="Chrome">Chrome</button>
  <button class="filter-btn" data-cat="Layout">Layout</button>
  <button class="filter-btn" data-cat="Sub">Sub</button>
  <button class="filter-btn" data-cat="CSS">CSS</button>
  <button class="filter-btn" data-cat="AI-BG">AI-BG</button>
  <button class="filter-btn" data-cat="Systems">Systems (___SYS___)</button>
  <span class="filter-sep"></span>
  <span class="filter-count">showing <span id="vis-count">___TOTAL___</span> / ___TOTAL___</span>
</div>

<nav id="nav">
___CARDS___
<div class="sys-section-header" data-cat="Systems" style="display:none">
  <span>Visual Systems</span>
</div>
___SYSCARDS___
</nav>

<main>
  <div class="preview-topbar">
    <div class="preview-path">gallery / <span id="preview-slug">—</span>.html</div>
    <div class="preview-actions">
      <a class="preview-btn" id="open-btn" href="#" target="_blank">open ↗</a>
    </div>
  </div>
  <div class="preview-frame">
    <div class="empty" id="empty">
      <div class="empty-prompt">← select a component<span class="cursor"></span></div>
      <div class="empty-sub">___TOTAL___ components · isolated + context demos</div>
    </div>
    <iframe name="preview" id="preview"></iframe>
  </div>
</main>

<script>
const nav   = document.getElementById('nav');
const empty = document.getElementById('empty');
const frame = document.getElementById('preview');
const slugEl = document.getElementById('preview-slug');
const openBtn = document.getElementById('open-btn');
const visCount = document.getElementById('vis-count');

function loadPreview(url, slug) {
  frame.style.opacity = '0';
  setTimeout(() => {
    frame.src = url;
    slugEl.textContent = slug.replace('.html','');
    openBtn.href = url;
    empty.style.display = 'none';
    frame.style.display = 'block';
    frame.onload = () => { frame.style.opacity = '1'; };
  }, 150);
}

function setActiveCard(card) {
  document.querySelectorAll('.card,.scard').forEach(c => c.classList.remove('active'));
  card.classList.add('active');
}

// ── Category filter ──────────────────────────────────────────────────
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('on'));
    btn.classList.add('on');
    const cat = btn.dataset.cat;
    let n = 0;
    document.querySelectorAll('.card,.scard').forEach(card => {
      const show = cat === 'all' || card.dataset.cat === cat;
      card.style.display = show ? '' : 'none';
      if (show) n++;
    });
    // Show/hide systems section header
    const sysHeader = document.querySelector('.sys-section-header');
    if (sysHeader) sysHeader.style.display = (cat === 'all' || cat === 'Systems') ? '' : 'none';
    visCount.textContent = n;
  });
});

// ── Card click (loads default component view) ────────────────────────
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('click', e => {
    if (e.target.closest('.ct-btn')) return;
    const mode = card.querySelector('.ct-btn.active')?.dataset.mode || 'component';
    const url = mode === 'context' ? card.dataset.context : card.dataset.component;
    const slug = url.split('/').pop();
    loadPreview(url, slug);
    setActiveCard(card);
  });
});

// ── Toggle buttons ───────────────────────────────────────────────────
document.querySelectorAll('.ct-btn').forEach(btn => {
  btn.addEventListener('click', e => {
    e.stopPropagation();
    const card = btn.closest('.card');
    card.querySelectorAll('.ct-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const mode = btn.dataset.mode;
    const url = mode === 'context' ? card.dataset.context : card.dataset.component;
    const slug = url.split('/').pop();
    loadPreview(url, slug);
    setActiveCard(card);
  });
});

// ── System card click ────────────────────────────────────────────────
document.querySelectorAll('.scard').forEach(card => {
  card.addEventListener('click', () => {
    const url = card.dataset.src;
    const slug = `sys-${card.dataset.slug}`;
    loadPreview(url, slug);
    setActiveCard(card);
  });
});

// ── Keyboard navigation ──────────────────────────────────────────────
document.addEventListener('keydown', e => {
  if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
  const visible = [...document.querySelectorAll('.card,.scard')].filter(c => c.style.display !== 'none');
  const active  = document.querySelector('.card.active,.scard.active');
  const idx     = visible.indexOf(active);
  let next;
  if (e.key === 'ArrowDown') next = visible[idx + 1] || visible[0];
  else                       next = visible[idx - 1] || visible[visible.length - 1];
  if (next) { next.scrollIntoView({block:'nearest'}); next.click(); }
  e.preventDefault();
});
</script>
</body>
</html>"""

    return template \
        .replace("___TOTAL___", str(total_n)) \
        .replace("___GEO___", str(geo_n)) \
        .replace("___CHROME___", str(chrome_n)) \
        .replace("___LAYOUT___", str(layout_n)) \
        .replace("___SUB___", str(sub_n)) \
        .replace("___CSS___", str(css_n)) \
        .replace("___AI___", str(ai_n)) \
        .replace("___SYS___", str(sys_n)) \
        .replace("___CARDS___", cards_joined) \
        .replace("___SYSCARDS___", syscards_joined)


# ─── Main ─────────────────────────────────────────────────────────────────────

def build_system_preview(sid: str, tok: dict, name: str) -> str:
    """Generate a self-contained system preview HTML — bg + colors + fonts."""
    bg      = tok.get("--bg-base", "#0a0a0a")
    bg_mid  = tok.get("--bg-mid",  "#111111")
    accent  = tok.get("--accent",  "#ffffff")
    txt     = tok.get("--text-primary", "#ffffff")
    fd_raw  = tok.get("--font-display", "'Inter'")
    fb_raw  = tok.get("--font-body",    "'Inter'")
    # Strip quotes for display and for font-family CSS value
    fd_clean = fd_raw.strip("'\"")
    fb_clean = fb_raw.strip("'\"")

    GFONTS = (
        "https://fonts.googleapis.com/css2?"
        "family=Archivo:wght@400;500;600;700"
        "&family=Cinzel+Decorative:wght@400;700"
        "&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,600"
        "&family=Crimson+Pro:wght@400;500;600"
        "&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,700;1,400"
        "&family=IBM+Plex+Sans:wght@400;500;600"
        "&family=Inter:wght@300;400;500;600;700"
        "&family=JetBrains+Mono:wght@300;400;500;700"
        "&family=Noto+Sans:wght@400;500;700"
        "&family=Noto+Sans+JP:wght@400;500;700"
        "&family=Noto+Serif:wght@400;500;600"
        "&family=Nunito:wght@400;500;600;700"
        "&family=Poppins:wght@400;500;600;700"
        "&family=Source+Serif+4:wght@400;500;600"
        "&family=Space+Grotesk:wght@300;400;500;600;700"
        "&family=Work+Sans:wght@400;500;600;700"
        "&display=swap"
    )

    num = sid[1:]  # "01" from "s01"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{sid} {name}</title>
<link href="{GFONTS}" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html,body{{height:100%;overflow:hidden}}
body{{
  background:linear-gradient(145deg,{bg},{bg_mid});
  color:{txt};
  font-family:'{fb_clean}',sans-serif;
  display:flex;flex-direction:column;height:100vh;
}}
.accent-bar{{height:3px;background:{accent};flex-shrink:0}}
.body{{flex:1;display:flex;flex-direction:column;padding:36px 44px;gap:0;overflow:hidden}}
.sys-id{{
  font-family:'JetBrains Mono',monospace;font-size:10px;
  letter-spacing:0.22em;text-transform:uppercase;
  color:{accent};opacity:0.75;margin-bottom:10px;
}}
.sys-name{{
  font-family:'{fd_clean}',sans-serif;font-size:clamp(36px,6vw,64px);
  font-weight:700;line-height:1.0;color:{txt};margin-bottom:18px;
}}
.sys-sample{{
  font-family:'{fb_clean}',sans-serif;font-size:14px;
  line-height:1.65;color:{txt};opacity:0.50;
  max-width:480px;margin-bottom:auto;padding-bottom:24px;
}}
.colors{{display:flex;gap:20px;align-items:flex-start;margin-bottom:24px;flex-shrink:0}}
.swatch{{display:flex;flex-direction:column;gap:5px}}
.swatch-box{{
  width:44px;height:44px;border-radius:6px;
  border:1px solid rgba(255,255,255,0.12);
}}
.swatch-role{{
  font-family:'JetBrains Mono',monospace;font-size:8px;
  letter-spacing:0.12em;text-transform:uppercase;
  color:{txt};opacity:0.35;
}}
.swatch-hex{{
  font-family:'JetBrains Mono',monospace;font-size:9px;
  color:{txt};opacity:0.55;
}}
.fonts{{
  border-top:1px solid rgba(255,255,255,0.08);
  padding-top:18px;display:grid;
  grid-template-columns:1fr 1fr;gap:14px;flex-shrink:0;
}}
.font-item{{display:flex;flex-direction:column;gap:3px}}
.font-role{{
  font-family:'JetBrains Mono',monospace;font-size:8px;
  letter-spacing:0.14em;text-transform:uppercase;
  color:{txt};opacity:0.35;
}}
.font-name{{font-size:13px;font-weight:600;color:{txt}}}
.font-name.display{{font-family:'{fd_clean}',sans-serif}}
.font-name.body{{font-family:'{fb_clean}',sans-serif}}
</style>
</head>
<body>
<div class="accent-bar"></div>
<div class="body">
  <div class="sys-id">{sid.upper()} · {name}</div>
  <div class="sys-name">{name}</div>
  <div class="sys-sample">
    El candidato ideal combina experiencia técnica con comunicación clara.<br>
    <em style="font-style:italic;opacity:0.7">The quick brown fox jumps — 0123456789</em>
  </div>
  <div class="colors">
    <div class="swatch">
      <div class="swatch-box" style="background:{accent}"></div>
      <div class="swatch-role">Accent</div>
      <div class="swatch-hex">{accent}</div>
    </div>
    <div class="swatch">
      <div class="swatch-box" style="background:{bg};border-color:rgba(255,255,255,0.25)"></div>
      <div class="swatch-role">Base</div>
      <div class="swatch-hex">{bg}</div>
    </div>
    <div class="swatch">
      <div class="swatch-box" style="background:{bg_mid};border-color:rgba(255,255,255,0.18)"></div>
      <div class="swatch-role">Mid</div>
      <div class="swatch-hex">{bg_mid}</div>
    </div>
  </div>
  <div class="fonts">
    <div class="font-item">
      <div class="font-role">Display</div>
      <div class="font-name display">{fd_clean}</div>
    </div>
    <div class="font-item">
      <div class="font-role">Body</div>
      <div class="font-name body">{fb_clean}</div>
    </div>
  </div>
</div>
</body>
</html>"""


def main():
    GALLERY.mkdir(parents=True, exist_ok=True)

    # Clean old gallery HTML files (keep INDEX.html for now)
    for old in GALLERY.glob("*.html"):
        if old.name != "INDEX.html":
            old.unlink()

    print(f"Building {len(DEMOS)} component demos in {GALLERY}/")
    errors = []
    for i, demo in enumerate(DEMOS, 1):
        n = f"{i:02d}"
        slug = demo["slug"]

        # ── Component view (isolated, dark s01) ─────────────────────────
        spec_comp = make_spec_component(demo)
        comp_path = GALLERY / f"{n}-{slug}-component.html"
        extras_comp = None
        for slide in spec_comp["slides"]:
            extras_comp = slide.pop("__extras", None)
        try:
            render_carousel(spec_comp, comp_path)
        except Exception as e:
            print(f"  [FAIL] {n}-{slug}-component: {e}", file=sys.stderr)
            errors.append(f"{slug}-component")
        else:
            if extras_comp:
                html = comp_path.read_text(encoding="utf-8")
                html = inject_extras(html, extras_comp)
                comp_path.write_text(html, encoding="utf-8")
            # Strip chrome/geo/decoratives for isolated view
            html = comp_path.read_text(encoding="utf-8")
            html = isolate_html(html, demo)
            comp_path.write_text(html, encoding="utf-8")

        # ── Context view (original system, real copy) ───────────────────
        spec_ctx = make_spec_context(demo)
        ctx_path = GALLERY / f"{n}-{slug}-context.html"
        extras_ctx = None
        for slide in spec_ctx["slides"]:
            extras_ctx = slide.pop("__extras", None)
        try:
            render_carousel(spec_ctx, ctx_path)
        except Exception as e:
            print(f"  [FAIL] {n}-{slug}-context: {e}", file=sys.stderr)
            errors.append(f"{slug}-context")
        else:
            if extras_ctx:
                html = ctx_path.read_text(encoding="utf-8")
                html = inject_extras(html, extras_ctx)
                ctx_path.write_text(html, encoding="utf-8")

        print(f"  [OK]  {n}-{slug}")

    # ── System previews ────────────────────────────────────────────────
    import json as _json
    comp_data_path = ROOT / "scripts" / "component_data.json"
    systems_list = []
    if comp_data_path.exists():
        try:
            comp_data = _json.loads(comp_data_path.read_text(encoding="utf-8-sig"))
            sys_data = comp_data.get("systems", {})
            for sid, tok in sorted(sys_data.items()):
                name = SYSTEM_NAMES.get(sid, sid.upper())
                sys_path = GALLERY / f"sys-{sid}.html"
                sys_path.write_text(build_system_preview(sid, tok, name), encoding="utf-8")
                systems_list.append({
                    "sid": sid,
                    "name": name,
                    "accent": tok.get("--accent", "#ffffff"),
                    "bg": tok.get("--bg-base", "#0a0a0a"),
                    "bg_mid": tok.get("--bg-mid", "#111111"),
                    "font_display": tok.get("--font-display", "'Inter'").strip("'\""),
                    "font_body": tok.get("--font-body", "'Inter'").strip("'\""),
                })
            print(f"  [SYS] {len(systems_list)} system previews generated")
        except Exception as e:
            print(f"  [WARN] Could not load component_data.json: {e}", file=sys.stderr)

    # ── INDEX ─────────────────────────────────────────────────────────
    index_path = GALLERY / "INDEX.html"
    index_path.write_text(build_index(DEMOS, systems_list), encoding="utf-8")

    print(f"\n[DONE] {len(DEMOS) * 2 - len(errors)}/{len(DEMOS) * 2} component demos rendered")
    print(f"       + {len(systems_list)} system previews")
    print(f"       INDEX -> {index_path}")
    if errors:
        print(f"  [FAIL] {len(errors)} failed: {', '.join(errors)}", file=sys.stderr)


if __name__ == "__main__":
    main()
