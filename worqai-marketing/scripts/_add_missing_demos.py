import sys

with open('scripts/build_gallery.py','r', encoding='utf-8') as f:
    content = f.read()

old = '''        "copy":{"kicker":"Dato clave","stat_number":"6x","stat_context":"más entrevistas con CV optimizado","headline":"El formato importa","body":"CVs ATS-optimizados obtienen 6 veces más respuestas."}}},
]


# ─── Total validation ──────────────────────────────────────────────────────────
assert len(DEMOS) == 101, f"Expected 101 demos, got {len(DEMOS)}"


def make_spec(demo: dict) -> dict:'''

if old not in content:
    print("ERROR: exact old string not found")
    sys.exit(1)

new_entries = """        "copy":{"kicker":"Dato clave","stat_number":"6x","stat_context":"más entrevistas con CV optimizado","headline":"El formato importa","body":"CVs ATS-optimizados obtienen 6 veces más respuestas."}}},

    # Core layouts missing from gallery
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

    # Original layers missing from gallery
    {"slug":"pw-grid","title":"PW Grid","tier":"1_geo","system":"s29","cat":"Geo","desc":"Cyberpunk wireframe background. Dark systems only.",
     "showcase":{"layout":"slide-big-number","layers":["pw-grid"],
        "copy":{"kicker":"Grid","stat_number":"01","stat_context":"wireframe base","headline":"Estructura digital"}}},
    {"slug":"scan-lines","title":"Scan Lines (Legacy)","tier":"1_geo","system":"s29","cat":"Geo","desc":"CRT scan-line overlay. Use geo-scan-lines for new builds.",
     "showcase":{"layout":"slide-terminal","layers":["scan-lines"],
        "copy":{"kicker":"Retro","headline":"Líneas de scan legacy","command":"scan --legacy","output_lines":[{"type":"ok","text":"✓ Compatible"}]}}},
    {"slug":"glow-orb","title":"Glow Orb","tier":"1_geo","system":"s04","cat":"Geo","desc":"Soft radial gradient bloom. Emotional / warm systems.",
     "showcase":{"layout":"slide-pull-quote-author","layers":["glow-orb"],
        "copy":{"kicker":"Warm","quote":"Un halo sutil cambia la percepción del contenido.","author":"Glow Note","role":"Atmósfera"}}},
    {"slug":"zoom-rings","title":"Zoom Rings","tier":"1_geo","system":"s17","cat":"Geo","desc":"Concentric focus burst. Shock / data emphasis.",
     "showcase":{"layout":"slide-big-number","layers":["zoom-rings"],
        "copy":{"kicker":"Focus","stat_number":"3x","stat_context":"más entrevistas","headline":"Impacto radial"}}},
    {"slug":"grid-bg","title":"Grid BG","tier":"1_geo","system":"s07","cat":"Geo","desc":"Brutalist grid background. Swiss / editorial.",
     "showcase":{"layout":"slide-hook-lockup","layers":["grid-bg"],
        "copy":{"kicker":"Grid","headline":"Estructura sin adornos.","body":"Grilla brutalista para sistemas editoriales."}}},
    {"slug":"diag-band","title":"Diag Band","tier":"1_geo","system":"s05","cat":"Geo","desc":"Diagonal accent band. Light systems.",
     "showcase":{"layout":"slide-big-number","layers":["diag-band"],
        "copy":{"kicker":"Light","stat_number":"45°","stat_context":"banda diagonal","headline":"Ángulo limpio"}}},
    {"slug":"blob-bg","title":"Blob BG","tier":"1_geo","system":"s04","cat":"Geo","desc":"DEPRECATED: ellipse blur blob. Use svg-blob-* instead.",
     "showcase":{"layout":"slide-pull-quote-author","layers":["blob-bg"],
        "copy":{"kicker":"Deprecated","quote":"El blob original era un ellipse + blur que html2canvas no captura.","author":"Note","role":"Legacy"}}},
    {"slug":"vol-light","title":"Vol Light","tier":"1_geo","system":"s17","cat":"Geo","desc":"Volumetric glow beams. Atmospheric depth.",
     "showcase":{"layout":"slide-big-number","layers":["vol-light"],
        "copy":{"kicker":"Depth","stat_number":"8","stat_context":"haces de luz","headline":"Volumetría"}}},

    # v2 Blob shapes missing from gallery
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

    # v3 Blob shapes missing from gallery
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

    # v3 Flow layers missing from gallery
    {"slug":"geo-flow-wave","title":"Flow Wave","tier":"1_geo","system":"s17","cat":"Geo","desc":"v3: sine-wave line spanning slide. Use with continuity:wave.",
     "showcase":{"layout":"slide-big-number","layers":["geo-flow-wave"],
        "copy":{"kicker":"Flow","stat_number":"~","stat_context":"onda continua","headline":"Sinusoide"}}},
    {"slug":"geo-flow-arrow","title":"Flow Arrow","tier":"1_geo","system":"s17","cat":"Geo","desc":"v3: large dashed arrow entering left. Progression signal.",
     "showcase":{"layout":"slide-hook-lockup","layers":["geo-flow-arrow"],
        "copy":{"kicker":"Arrow","headline":"Progresión implícita.","body":"Una flecha que apunta hacia adelante sin palabras."}}},
    {"slug":"geo-flow-data","title":"Flow Data","tier":"1_geo","system":"s29","cat":"Geo","desc":"v3: dotted particle trail with nodes. Tech continuity.",
     "showcase":{"layout":"slide-terminal","layers":["geo-flow-data","pw-grid"],
        "copy":{"kicker":"Pipeline","headline":"Datos en movimiento","command":"flow --status","output_lines":[{"type":"ok","text":"● Node 1 active"},{"type":"ok","text":"● Node 2 active"},{"type":"warn","text":"○ Node 3 idle"}]}}},

    # Decoratives missing from gallery
    {"slug":"watermark","title":"Watermark","tier":"4_sub","system":"s17","cat":"Sub","desc":"Giant faint letter/symbol behind content.",
     "showcase":{"layout":"slide-big-number","layers":["geo-halftone"],
        "decoratives":["watermark"],
        "copy":{"kicker":"Watermark","stat_number":"W","stat_context":"marca fantasma","headline":"Sello sutil"}}},
]


# ─── Total validation ──────────────────────────────────────────────────────────
assert len(DEMOS) == 128, f"Expected 128 demos, got {len(DEMOS)}"


def make_spec(demo: dict) -> dict:"""

content = content.replace(old, new_entries)
with open('scripts/build_gallery.py','w', encoding='utf-8') as f:
    f.write(content)
print('OK, appended 27 missing entries. Total demos now:', content.count('"slug":'))
