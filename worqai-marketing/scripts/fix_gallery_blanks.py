#!/usr/bin/env python3
"""
fix_gallery_blanks.py
=====================
Fixes all blank gallery component files:

Phase 1 — Layout files (46-97) + CSS files (120-122):
  Remove the wrapper-hiding CSS block so layout wrappers become visible.

Phase 2 — Sub-component files (99-116):
  Insert actual sub-component HTML as a direct child of .slide so the
  component is isolated and centered by the existing centering CSS.
"""

import os, re

GALLERY = r"c:\Users\kenne\OneDrive\Documentos\worqai-marketing\gallery"

# ─────────────────────────────────────────────────────────────────────────────
# The exact CSS block (9 lines) to REMOVE from layout files
# ─────────────────────────────────────────────────────────────────────────────
WRAPPER_HIDE_BLOCK = """.hook-wrap, .stat-wrap, .term-wrap, .tip-wrap, .ba-wrap, .chk-wrap,
.proof-wrap, .cta-wrap, .quote-wrap, .step-wrap, .bento-wrap, .grid-wrap,
.compare-wrap, .comp-table-wrap, .faq-wrap, .timeline-wrap, .warn-wrap,
.poster-wrap, .mvf-wrap, .cascade-wrap, .statrow-wrap, .qauth-wrap,
.pbar-wrap, .lnum-wrap, .donut-wrap, .fbt-wrap, .diags-wrap, .asym-wrap,
.tos-wrap, .stype-wrap, .cman-wrap, .dwall-wrap, .sbs-wrap, .fwf-wrap,
.mn-wrap, .tfs-wrap, .ec-wrap, .badgeg-wrap, .ck-wrap, .cq-wrap, .wfl-wrap,
.at-wrap, .mcs-wrap, .lw-wrap, .rcpt-wrap, .pg-wrap, .tc-wrap, .mc-wrap,
.sc-wrap, .io-wrap, .waffle-wrap, .bas-wrap, .conn-wrap, .icong-wrap { display: none !important; }"""

# ─────────────────────────────────────────────────────────────────────────────
# Layout file numbers (remove wrapper-hide block so content shows)
# ─────────────────────────────────────────────────────────────────────────────
LAYOUT_NUMS = list(range(46, 98)) + [120, 121, 122]

# ─────────────────────────────────────────────────────────────────────────────
# Sub-component demo HTML to INSERT as direct child of .slide
# (inserted between <div class="slide active"> and <div class="comp-label")
# ─────────────────────────────────────────────────────────────────────────────
SUB_DEMOS = {

    99:  # pill-tag
        '  <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;'
        'justify-content:center;padding:20px;">\n'
        '    <span class="sub-pill-tag">ATS</span>\n'
        '    <span class="sub-pill-tag">Español</span>\n'
        '    <span class="sub-pill-tag solid">Aprobado</span>\n'
        '  </div>',

    100:  # arrow-flow
        '  <div style="display:flex;align-items:center;gap:24px;justify-content:center;">\n'
        '    <span style="font-family:var(--font-display);font-size:14px;'
        'color:var(--text-primary);">Score 12</span>\n'
        '    <div class="sub-arrow-flow"></div>\n'
        '    <span style="font-family:var(--font-display);font-size:14px;'
        'color:var(--accent);">Score 84</span>\n'
        '  </div>',

    101:  # icon-circle
        '  <div style="display:flex;gap:16px;align-items:center;justify-content:center;flex-wrap:wrap;">\n'
        '    <div class="sub-icon-circle">'
        '<svg class="icon" aria-hidden="true" width="20" height="20"><use href="#icon-star"/></svg></div>\n'
        '    <div class="sub-icon-circle solid">'
        '<svg class="icon" aria-hidden="true" width="20" height="20"><use href="#icon-ok"/></svg></div>\n'
        '    <div class="sub-icon-circle">'
        '<svg class="icon" aria-hidden="true" width="20" height="20"><use href="#icon-arrow-right"/></svg></div>\n'
        '  </div>',

    102:  # dotted-divider
        '  <div style="display:flex;flex-direction:column;gap:14px;width:280px;align-items:stretch;">\n'
        '    <div style="font-family:var(--font-display);font-size:13px;'
        'color:var(--text-muted);">Antes</div>\n'
        '    <div class="sub-dotted-divider"></div>\n'
        '    <div style="font-family:var(--font-display);font-size:13px;'
        'color:var(--accent);">Después</div>\n'
        '  </div>',

    103:  # rating-stars
        '  <div style="display:flex;flex-direction:column;align-items:center;gap:10px;">\n'
        '    <div class="sub-rating-stars"></div>\n'
        '    <div style="font-family:var(--font-display);font-size:12px;'
        'color:var(--text-muted);letter-spacing:0.08em;">4.9 · 2,847 usuarios</div>\n'
        '  </div>',

    104:  # logo-row
        '  <div class="sub-logo-row" style="justify-content:center;flex-wrap:wrap;">\n'
        '    <span class="logo">LinkedIn</span>\n'
        '    <span class="logo">Google</span>\n'
        '    <span class="logo">Meta</span>\n'
        '    <span class="logo">WorqAI</span>\n'
        '  </div>',

    105:  # avatar-stack
        '  <div style="display:flex;align-items:center;gap:14px;justify-content:center;">\n'
        '    <div class="sub-avatar-stack">\n'
        '      <div class="av">A</div>\n'
        '      <div class="av">B</div>\n'
        '      <div class="av">C</div>\n'
        '      <div class="av more">+84</div>\n'
        '    </div>\n'
        '    <span style="font-family:var(--font-display);font-size:13px;'
        'color:var(--text-muted);">ya lo usan</span>\n'
        '  </div>',

    106:  # fact-bubble
        '  <div style="display:flex;flex-direction:column;gap:10px;width:340px;">\n'
        '    <div class="sub-fact-bubble myth">\n'
        '      <span class="bub-label">Mito</span>\n'
        '      <span class="mvf-text">Mandar 100 apps aumenta tus chances.</span>\n'
        '    </div>\n'
        '    <div class="sub-fact-bubble fact">\n'
        '      <span class="bub-label">Realidad</span>\n'
        '      <span class="mvf-text">3 aplicaciones segmentadas convierten más.</span>\n'
        '    </div>\n'
        '  </div>',

    107:  # timeline-dot
        '  <div style="display:flex;align-items:center;gap:14px;justify-content:center;">\n'
        '    <div class="sub-timeline-dot"></div>\n'
        '    <div style="width:40px;height:1px;background:var(--accent);opacity:0.4;"></div>\n'
        '    <div class="sub-timeline-dot"></div>\n'
        '    <div style="width:40px;height:1px;background:var(--accent);opacity:0.4;"></div>\n'
        '    <div class="sub-timeline-dot"></div>\n'
        '  </div>',

    108:  # bento-card
        '  <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">\n'
        '    <div class="sub-bento-card" style="min-width:120px;">\n'
        '      <div class="bento-label">Score</div>\n'
        '      <div class="bento-title">87</div>\n'
        '      <div class="bento-body">ATS Ready</div>\n'
        '    </div>\n'
        '    <div class="sub-bento-card accent" style="min-width:120px;">\n'
        '      <div class="bento-label">Entrevistas</div>\n'
        '      <div class="bento-title">4</div>\n'
        '      <div class="bento-body">Esta semana</div>\n'
        '    </div>\n'
        '  </div>',

    109:  # inline-stat
        '  <p style="font-family:var(--font-body);font-size:18px;color:var(--text-primary);'
        'line-height:1.65;text-align:center;max-width:340px;">\n'
        '    De <span class="sub-inline-stat">40</span> apps enviadas,\n'
        '    solo <span class="sub-inline-stat">2</span> respondieron.\n'
        '  </p>',

    110:  # status-pill
        '  <div style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;'
        'justify-content:center;">\n'
        '    <div class="sub-status-pill pass">Aprobado</div>\n'
        '    <div class="sub-status-pill warn">En revisión</div>\n'
        '    <div class="sub-status-pill fail">Rechazado</div>\n'
        '  </div>',

    111:  # comment-mock
        '  <div class="sub-comment-mock" style="max-width:360px;">\n'
        '    <div class="com-av">K</div>\n'
        '    <div class="com-body">\n'
        '      <div class="com-handle">@worqai</div>\n'
        '      <div class="com-text">Mi CV pasó el ATS en 48 horas ✓</div>\n'
        '    </div>\n'
        '  </div>',

    112:  # handle-line
        '  <div class="sub-handle-line">\n'
        '    <span class="handle">@worqai</span>\n'
        '    <span class="dot">·</span>\n'
        '    <span>worqai.com</span>\n'
        '    <span class="dot">·</span>\n'
        '    <span>2h</span>\n'
        '  </div>',

    113:  # stat-card
        '  <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;">\n'
        '    <div class="sub-stat-card" style="min-width:120px;">\n'
        '      <div class="sc-num">87</div>\n'
        '      <div class="sc-label">ATS Score</div>\n'
        '      <div class="sc-body">Promedio WorqAI</div>\n'
        '    </div>\n'
        '    <div class="sub-stat-card" style="min-width:120px;">\n'
        '      <div class="sc-num">48h</div>\n'
        '      <div class="sc-label">Entrevista</div>\n'
        '      <div class="sc-body">Tiempo promedio</div>\n'
        '    </div>\n'
        '  </div>',

    114:  # chip-list
        '  <div class="sub-chip-list" style="justify-content:center;max-width:320px;">\n'
        '    <span class="chip">JavaScript</span>\n'
        '    <span class="chip">Python</span>\n'
        '    <span class="chip">React</span>\n'
        '    <span class="chip">Node.js</span>\n'
        '    <span class="chip">+3 más</span>\n'
        '  </div>',

    115:  # download-card
        '  <div class="sub-download-card">\n'
        '    <div class="dl-icon">PDF</div>\n'
        '    <div class="dl-body">\n'
        '      <div class="dl-title">CV Optimizado</div>\n'
        '      <div class="dl-sub">PDF · ATS Ready · Español</div>\n'
        '    </div>\n'
        '  </div>',

    116:  # emoji-callout
        '  <div class="sub-emoji-callout">\n'
        '    <div class="ec-emoji">🎯</div>\n'
        '    <div class="ec-text">Tu CV llega al reclutador</div>\n'
        '  </div>',
}


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def file_for_num(num):
    """Return the full path of the component file for a given number, or None."""
    for fname in os.listdir(GALLERY):
        if fname.startswith(f"{num}-") and fname.endswith("-component.html"):
            return os.path.join(GALLERY, fname)
    return None


def fix_layout(filepath):
    """Remove the wrapper-hiding CSS block from a layout file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if WRAPPER_HIDE_BLOCK not in content:
        print(f"  SKIP  (no hide block): {os.path.basename(filepath)}")
        return False

    # Remove the block plus its trailing newline
    new_content = content.replace(WRAPPER_HIDE_BLOCK + "\n", "", 1)
    if new_content == content:                          # fallback: no trailing \n
        new_content = content.replace(WRAPPER_HIDE_BLOCK, "", 1)

    if new_content == content:
        print(f"  WARN  (replace failed): {os.path.basename(filepath)}")
        return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  FIXED layout : {os.path.basename(filepath)}")
    return True


def fix_sub(filepath, num):
    """Insert demo HTML as a direct child of the slide element."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    demo = SUB_DEMOS.get(num)
    if not demo:
        print(f"  SKIP  (no demo defined): {os.path.basename(filepath)}")
        return False

    # Guard: already patched?
    sentinel = demo.split("\n")[0].strip()[:40]
    if sentinel in content:
        print(f"  SKIP  (already patched): {os.path.basename(filepath)}")
        return False

    # Insert point: between '<div class="slide active">' and '  <div class="comp-label"'
    old_anchor = '<div class="slide active">\n  <div class="comp-label"'
    new_anchor = f'<div class="slide active">\n{demo}\n  <div class="comp-label"'

    if old_anchor not in content:
        print(f"  WARN  (anchor not found): {os.path.basename(filepath)}")
        return False

    new_content = content.replace(old_anchor, new_anchor, 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  FIXED sub-comp: {os.path.basename(filepath)}")
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    ok = fail = skip = 0

    print("=" * 60)
    print("PHASE 1 — Remove wrapper-hide CSS from layout files")
    print("=" * 60)
    for num in LAYOUT_NUMS:
        fp = file_for_num(num)
        if not fp:
            print(f"  NOT FOUND: #{num}")
            fail += 1
            continue
        result = fix_layout(fp)
        if result is True:
            ok += 1
        elif result is False:
            skip += 1  # SKIP or WARN counted together for now

    print()
    print("=" * 60)
    print("PHASE 2 — Insert demo HTML into sub-component files")
    print("=" * 60)
    for num in sorted(SUB_DEMOS.keys()):
        fp = file_for_num(num)
        if not fp:
            print(f"  NOT FOUND: #{num}")
            fail += 1
            continue
        result = fix_sub(fp, num)
        if result is True:
            ok += 1
        else:
            skip += 1

    print()
    print(f"Done — {ok} fixed, {skip} skipped/warned, {fail} not found.")


if __name__ == "__main__":
    main()
