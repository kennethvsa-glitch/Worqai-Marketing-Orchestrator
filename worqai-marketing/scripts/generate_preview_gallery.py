#!/usr/bin/env python3
"""
generate_preview_gallery.py
Reads all component files and generates a single preview-gallery.html
that renders all 180 components in iframe cards with theme switching.
"""

import json
from pathlib import Path

COMPONENTS_DIR = Path(".claude/skills/html-carousel-builder/components")
OUTPUT_PATH = Path(".claude/skills/html-carousel-builder/preview-gallery.html")

THEMES = {
    "dark": {
        "name": "Dark (s04 Crimson)",
        "bg_base": "#0a0608", "bg_mid": "#140a10", "bg_highlight": "#1e1018",
        "text_primary": "#FFFFFF", "text_secondary": "#d0c0c8", "text_muted": "#806070",
        "accent": "#e05a7a", "accent_soft": "rgba(224,90,122,0.12)", "accent_line": "rgba(224,90,122,0.25)",
        "font_display": "'Poppins'", "font_body": "'Poppins'", "font_mono": "'JetBrains Mono'",
        "pad_x": "80px", "pad_y": "96px", "pad_bottom_safe": "140px",
        "grain_opacity": "0.05", "geo_opacity": "0.08", "glow_opacity": "0.12",
    },
    "light": {
        "name": "Light (s25 Swiss Brut)",
        "bg_base": "#ffffff", "bg_mid": "#f5f5f5", "bg_highlight": "#eeeeee",
        "text_primary": "#111111", "text_secondary": "#555555", "text_muted": "#999999",
        "accent": "#ff0015", "accent_soft": "rgba(255,0,21,0.08)", "accent_line": "rgba(255,0,21,0.20)",
        "font_display": "'Archivo'", "font_body": "'Archivo'", "font_mono": "'JetBrains Mono'",
        "pad_x": "80px", "pad_y": "96px", "pad_bottom_safe": "140px",
        "grain_opacity": "0.15", "geo_opacity": "0.06", "glow_opacity": "0.08",
    },
    "accent": {
        "name": "Accent (s17 WorqAI)",
        "bg_base": "#1A1A18", "bg_mid": "#252520", "bg_highlight": "#303028",
        "text_primary": "#FFF8E7", "text_secondary": "#d0c8b8", "text_muted": "#887860",
        "accent": "#C7FF3A", "accent_soft": "rgba(199,255,58,0.10)", "accent_line": "rgba(199,255,58,0.25)",
        "font_display": "'Nunito'", "font_body": "'Nunito'", "font_mono": "'JetBrains Mono'",
        "pad_x": "80px", "pad_y": "96px", "pad_bottom_safe": "140px",
        "grain_opacity": "0.05", "geo_opacity": "0.10", "glow_opacity": "0.12",
    },
}


def collect_components():
    categories = {"layers": [], "slides": [], "decorative": [], "mock-ui": []}
    for cat in categories:
        cat_dir = COMPONENTS_DIR / cat
        if not cat_dir.exists():
            continue
        for filepath in sorted(cat_dir.rglob("*.html")):
            rel_path = filepath.relative_to(COMPONENTS_DIR)
            content = filepath.read_text(encoding="utf-8")
            categories[cat].append({
                "name": filepath.stem,
                "path": str(rel_path).replace("\\", "/"),
                "content": content,
            })
    return categories


def generate_iframe_srcdoc(component_content, theme):
    css_vars = f""":root {{
  --bg-base: {theme['bg_base']};
  --bg-mid: {theme['bg_mid']};
  --bg-highlight: {theme['bg_highlight']};
  --text-primary: {theme['text_primary']};
  --text-secondary: {theme['text_secondary']};
  --text-muted: {theme['text_muted']};
  --accent: {theme['accent']};
  --accent-soft: {theme['accent_soft']};
  --accent-line: {theme['accent_line']};
  --font-display: {theme['font_display']};
  --font-body: {theme['font_body']};
  --font-mono: {theme['font_mono']};
  --pad-x: {theme['pad_x']};
  --pad-y: {theme['pad_y']};
  --pad-bottom-safe: {theme['pad_bottom_safe']};
  --grain-opacity: {theme['grain_opacity']};
  --geo-opacity: {theme['geo_opacity']};
  --glow-opacity: {theme['glow_opacity']};
}}"""
    doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&family=Archivo:wght@400;600;700;900&family=Nunito:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{height:100%;background:var(--bg-base);}}
body{{font-family:var(--font-body),system-ui,sans-serif;}}
.preview-shell{{
  position:relative;
  width:100%;height:100%;
  background:var(--bg-base);
  overflow:hidden;
}}
</style>
<style>{css_vars}</style>
</head>
<body>
<div class="preview-shell">
{component_content}
</div>
</body>
</html>"""
    return doc


def generate_gallery_html(categories):
    js_components = []
    for cat_name, items in categories.items():
        for item in items:
            js_components.append({
                "category": cat_name,
                "name": item["name"],
                "path": item["path"],
                "srcdocs": {
                    theme_key: generate_iframe_srcdoc(item["content"], theme)
                    for theme_key, theme in THEMES.items()
                }
            })

    components_json = json.dumps(js_components, ensure_ascii=False)

    cat_config = json.dumps({
        "layers": {"title": "LAYERS", "subtitle": "Background Atmosphere (60)", "w": 400, "h": 400},
        "slides": {"title": "SLIDES", "subtitle": "Content Layouts (60)", "w": 360, "h": 360},
        "decorative": {"title": "DECORATIVE", "subtitle": "Flourishes & Accents (30)", "w": 320, "h": 320},
        "mock-ui": {"title": "MOCK-UI", "subtitle": "Interface Simulations (30)", "w": 360, "h": 360},
    })

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Component Preview Gallery - 180 Components</title>
<style>
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  body{{
    font-family:system-ui,-apple-system,sans-serif;
    background:#0a0a0a;
    color:#e0e0e0;
    line-height:1.5;
  }}
  .header{{
    position:sticky;top:0;z-index:100;
    background:rgba(10,10,10,0.95);
    backdrop-filter:blur(12px);
    border-bottom:1px solid #222;
    padding:20px 32px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    flex-wrap:wrap;
    gap:16px;
  }}
  .header h1{{font-size:18px;font-weight:700;letter-spacing:-0.02em}}
  .header .count{{font-size:12px;color:#666;margin-left:8px;font-weight:400}}
  .themes{{display:flex;gap:8px;}}
  .theme-btn{{
    padding:8px 16px;border-radius:6px;border:1px solid #333;
    background:#1a1a1a;color:#888;font-size:12px;font-weight:600;
    cursor:pointer;transition:all 0.15s;
  }}
  .theme-btn:hover{{border-color:#555;color:#ccc}}
  .theme-btn.active{{border-color:var(--active-accent,#e05a7a);color:#fff;background:#222}}
  .main{{padding:24px 32px 64px;max-width:1600px;margin:0 auto;}}
  .section{{margin-bottom:48px;}}
  .section-header{{
    display:flex;align-items:baseline;gap:12px;
    margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid #222;
  }}
  .section-title{{font-size:14px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#888}}
  .section-count{{font-size:12px;color:#555}}
  .grid{{
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(220px,1fr));
    gap:20px;
  }}
  .card{{
    background:#111;border:1px solid #222;border-radius:10px;
    overflow:hidden;transition:border-color 0.15s;
  }}
  .card:hover{{border-color:#444}}
  .card-header{{
    padding:10px 12px;border-bottom:1px solid #1a1a1a;
    display:flex;align-items:center;justify-content:space-between;
  }}
  .card-name{{
    font-size:11px;font-weight:600;color:#aaa;
    font-family:'JetBrains Mono',monospace;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
  }}
  .card-path{{
    font-size:9px;color:#444;
    font-family:'JetBrains Mono',monospace;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
  }}
  .card-body{{
    background:#0a0a0a;
    display:flex;align-items:center;justify-content:center;
    position:relative;
  }}
  .card-body iframe{{
    border:none;display:block;
    width:100%;height:100%;
  }}
  .loading{{
    position:absolute;inset:0;
    display:flex;align-items:center;justify-content:center;
    color:#333;font-size:11px;
  }}
</style>
</head>
<body>
<div class="header">
  <h1>Component Preview Gallery<span class="count">180 components</span></h1>
  <div class="themes">
    <button class="theme-btn active" data-theme="dark" onclick="setTheme('dark')">Dark (s04)</button>
    <button class="theme-btn" data-theme="light" onclick="setTheme('light')">Light (s25)</button>
    <button class="theme-btn" data-theme="accent" onclick="setTheme('accent')">Accent (s17)</button>
  </div>
</div>
<div class="main" id="main"></div>

<script>
const COMPONENTS = {components_json};
const CAT_CONFIG = {cat_config};
let currentTheme = 'dark';

function setTheme(theme) {{
  currentTheme = theme;
  document.querySelectorAll('.theme-btn').forEach(b => b.classList.toggle('active', b.dataset.theme === theme));
  const accentMap = {{dark:'#e05a7a', light:'#ff0015', accent:'#C7FF3A'}};
  document.documentElement.style.setProperty('--active-accent', accentMap[theme]);
  document.querySelectorAll('iframe[data-idx]').forEach(ifr => {{
    const idx = parseInt(ifr.dataset.idx);
    ifr.srcdoc = COMPONENTS[idx].srcdocs[theme];
  }});
}}

function render() {{
  const main = document.getElementById('main');
  main.innerHTML = '';
  const groups = {{}};
  COMPONENTS.forEach((c, i) => {{
    if (!groups[c.category]) groups[c.category] = [];
    groups[c.category].push({{...c, _idx: i}});
  }});
  Object.keys(CAT_CONFIG).forEach(catKey => {{
    const items = groups[catKey] || [];
    const cfg = CAT_CONFIG[catKey];
    const section = document.createElement('div');
    section.className = 'section';
    section.innerHTML = `
      <div class="section-header">
        <span class="section-title">${{cfg.title}}</span>
        <span class="section-count">${{items.length}} components</span>
      </div>
      <div class="grid" id="grid-${{catKey}}"></div>
    `;
    main.appendChild(section);
    const grid = section.querySelector('.grid');
    items.forEach(item => {{
      const card = document.createElement('div');
      card.className = 'card';
      const h = cfg.h;
      card.innerHTML = `
        <div class="card-header">
          <span class="card-name" title="${{item.name}}">${{item.name}}</span>
        </div>
        <div class="card-body" style="height:${{h}}px;">
          <div class="loading">Loading...</div>
          <iframe data-idx="${{item._idx}}" sandbox="allow-same-origin" style="display:none;" loading="lazy"></iframe>
        </div>
        <div class="card-header">
          <span class="card-path" title="${{item.path}}">${{item.path}}</span>
        </div>
      `;
      grid.appendChild(card);
      const ifr = card.querySelector('iframe');
      const loading = card.querySelector('.loading');
      requestAnimationFrame(() => {{
        ifr.srcdoc = item.srcdocs[currentTheme];
        ifr.style.display = 'block';
        if (loading) loading.style.display = 'none';
      }});
    }});
  }});
}}
render();
</script>
</body>
</html>"""
    return html


def main():
    print("Scanning components...")
    categories = collect_components()
    total = sum(len(v) for v in categories.values())
    print(f"Found {total} components:")
    for cat, items in categories.items():
        print(f"  {cat}: {len(items)}")
    print("\nGenerating preview gallery...")
    html = generate_gallery_html(categories)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(html, encoding="utf-8")
    size_kb = len(html) / 1024
    print(f"\nDone: {OUTPUT_PATH}")
    print(f"File size: {size_kb:.1f} KB")
    print("Open this file in any browser to preview all components.")


if __name__ == "__main__":
    main()
