---
name: carousel-to-zip-exporter
description: >
  FALLBACK EXPORTER — use only when the in-HTML ZIP export (html2canvas + JSZip button built
  into every carousel) produces rendering errors (blurry output, misrendered glassmorphism,
  broken backdrop-filter). This skill uses Playwright/Chromium for pixel-perfect rendering of
  any CSS. For standard carousels without heavy CSS effects, use the ZIP button in the HTML instead
  — it requires no Python setup and saves tokens. When routing here, tell the user why html2canvas
  failed so they understand the fallback.
metadata:
  author: kenneth-valverde
  version: 1.0
  domain: ad-creative-production
  language: es-CR / en
---

## What This Skill Does

Takes a completed HTML carousel file (from html-carousel-builder or any source) and outputs a ZIP file containing one PNG per slide, numbered sequentially, ready to upload directly to Instagram or Facebook as a carousel post.

Fonts, colors, spacing, and layout from the HTML are preserved pixel-for-pixel in every exported image. No redesign. No reinterpretation. What you see in the browser is what gets exported.

---

## When to Use This Skill

Use ONLY when the in-HTML ZIP export has already failed or cannot be used:

- User reports that the in-HTML ZIP button produced blurry, misrendered, or blank slides
- The carousel uses glassmorphism (`backdrop-filter`), heavy SVG displacement, or complex blend modes that html2canvas cannot render
- User explicitly asks to run `carousel_exporter.py` directly
- User is in an environment without a browser (headless CI, server-side rendering)

**Do NOT use this skill** if the user just wants to export a standard carousel — tell them to use the ZIP button in the HTML. It requires no setup and produces correct output for most carousels.

## When the In-HTML ZIP Button Works (most cases)

Every carousel HTML built after May 2026 has a ZIP export button using html2canvas + JSZip. It handles:
- All gradient backgrounds
- SVG grain textures
- Cormorant Garamond + Raleway + DM Sans fonts (loaded via Google Fonts CDN)
- Photo upload zones (backgroundImage via FileReader)
- Standard box shadows and border-radius

Route to this skill only when one of the above failure conditions is confirmed.

---

## Inputs Required

Before running, collect:

1. **HTML carousel file or code** — the complete self-contained HTML (required). Accept as file upload or pasted code block.
2. **Slide dimensions** — default 1080×1080px (square). Accept 1080×1350px (4:5) or 1080×1920px (9:16) if specified.
3. **Output filename prefix** — default: `slide`. Output files will be named `slide_01.png`, `slide_02.png`, etc. User can specify a custom prefix (e.g., `carrusel_cv`, `post_linkedin`).
4. **ZIP file name** — default: `carousel_export.zip`. User can specify a custom name.

If the HTML is missing, stop and ask for it. Never generate placeholder images.

---

## Step-by-Step Workflow

1. **Receive HTML input.** Accept as file upload (.html) or as a pasted code block. If pasted, save it as a temp `.html` file.

2. **Detect slide count.** Parse the HTML to count the number of slides (look for `.slide`, `[data-slide]`, or the slide container structure used by html-carousel-builder). Log the count before proceeding.

3. **Extract font dependencies.** Scan the HTML for Google Fonts `@import` or `<link>` tags. Pass these to the Python renderer so fonts load correctly in the headless browser. If fonts are loaded via CDN, the renderer must have internet access or local fallback fonts must be mapped.

4. **Render each slide to PNG.** Use the Python script (`carousel_exporter.py`) to:
   - Launch a headless Chromium browser via Playwright
   - Navigate to each slide by index (show one slide at a time using JS)
   - Set the viewport to match the slide dimensions
   - Take a full-page screenshot of the visible slide area only
   - Save as `slide_01.png`, `slide_02.png`, etc. (zero-padded, starting at 01)

5. **Verify output.** After all slides are exported, check:
   - File count matches detected slide count
   - All files are non-zero size
   - Naming is sequential with no gaps

6. **Package into ZIP.** Create `carousel_export.zip` (or user-specified name) containing all numbered PNG files and nothing else. No subfolders inside the ZIP.

7. **Deliver.** Output the ZIP file as a downloadable artifact. Confirm slide count and ZIP name in the response.

---

## Output Format

```
carousel_export.zip
├── slide_01.png    ← First slide (hook)
├── slide_02.png    ← Second slide
├── slide_03.png
├── slide_04.png
├── slide_05.png
├── slide_06.png
├── slide_07.png
└── slide_08.png    ← Last slide (CTA)
```

- File format: PNG (lossless, Instagram-safe)
- Dimensions: match HTML canvas exactly (default 1080×1080px)
- Naming: `[prefix]_[zero-padded number].png` → `slide_01.png`, `slide_08.png`
- ZIP contains only the PNG files — no HTML, no temp files, no subfolders
- ZIP name: `carousel_export.zip` by default, customizable

---

## Font Preservation Rules

Fonts must match the HTML exactly. Apply these rules in order:

1. If the HTML loads Google Fonts via CDN link, the Playwright renderer fetches them during page load (internet required). No action needed.
2. If the HTML uses `@font-face` with local files, those font files must be in the same directory as the HTML file before rendering.
3. If internet is unavailable and CDN fonts cannot load, map to these local fallbacks:
   - Inter → system-ui, -apple-system, sans-serif
   - Poppins → system-ui, -apple-system, sans-serif
   - Montserrat → system-ui, -apple-system, sans-serif
4. Never substitute a serif or monospace font for a sans-serif design font.
5. After rendering, visually verify Slide 1 to confirm headline font weight and size are correct before exporting all slides.

---

## Design Token Preservation Rules

The exporter must not alter any visual property from the HTML:

- Background colors: hex values must be identical in output
- Text colors: no color shift from headless rendering
- Font sizes: viewport must match the HTML canvas size exactly so `px` values render 1:1
- Spacing and padding: no layout reflow — set browser zoom to 1.0, no scaling
- Slide counter element: hide it before screenshot if user requests clean slides (default: keep visible)
- Navigation arrows: always hide before taking screenshots (they are UI chrome, not content)

---

## Quality Checklist

Before delivering the ZIP, verify:

- [ ] Slide count in ZIP matches slide count detected in HTML
- [ ] All PNG files are non-zero size (no blank exports)
- [ ] File names are zero-padded and sequential: `slide_01`, `slide_02`... no `slide_1` or `slide_9` without padding
- [ ] Fonts match the HTML — no fallback substitution unless CDN was unreachable
- [ ] Navigation arrows and UI chrome are hidden in all exported images
- [ ] Background colors match the HTML source (spot-check slide 1 and last slide)
- [ ] ZIP contains only PNG files — no HTML source, no temp files, no `.DS_Store`
- [ ] ZIP file is not empty and opens correctly

---

## Rules

1. Never export slides without the actual HTML source. Do not generate placeholder or dummy images.
2. The Python script (`carousel_exporter.py`) is the only tool used for rendering. Do not use canvas2image, html2canvas JS libraries, or server-side screenshot APIs.
3. Always hide navigation arrows and swipe indicators before screenshotting. These are UI elements, not slide content.
4. Slide counter (e.g., "3 / 8") is kept visible by default. User can request it be hidden.
5. File numbering always starts at `01`, not `0` or `1`. Always zero-pad to two digits minimum.
6. If the carousel has more than 99 slides, zero-pad to three digits: `slide_001.png`.
7. ZIP must be flat — no subdirectories inside the archive.
8. If a slide fails to render (blank, error, timeout), log the slide number, skip it, and report which slides failed in the final response.
9. Default dimensions are 1080×1080px. If the HTML specifies a different canvas size in CSS, detect it automatically and use it.
10. Never rewrite, reinterpret, or redesign any element of the HTML. Export only what the browser renders.

---

## Error Handling

| Problem | Action |
|---|---|
| HTML has no detectable slides | Ask user to confirm slide selector (`.slide`, `.carousel-item`, etc.) |
| Google Fonts CDN unreachable | Use system font fallback, notify user in response |
| Slide renders blank (white or black) | Check if slide visibility CSS needs JS activation — use `carousel_exporter.py` show-slide function |
| ZIP file exceeds 50MB | Compress PNGs at 90% quality, notify user |
| Playwright not installed | Script auto-installs via `pip install playwright` + `playwright install chromium` |

---

## Integration with html-carousel-builder

This skill is the fallback export layer for html-carousel-builder. Standard flow:

1. `html-carousel-builder` produces the self-contained HTML carousel
2. User attempts export via the in-HTML ZIP button (html2canvas + JSZip)
3. If that button fails (glassmorphism, complex backdrop-filter), user triggers `carousel-to-zip-exporter` with the HTML file
4. Exporter produces the numbered PNG ZIP via headless Chromium
5. User uploads ZIP directly to Instagram/Facebook carousel post

No manual redesign step. No Canva export. No screenshot-by-hand process.

---

## Companion Script

`carousel_exporter.py` — run this script directly or let the AI execute it.

See `carousel_exporter.py` for the full implementation. The script handles:
- Playwright headless rendering
- Slide detection and isolation
- Navigation chrome removal
- Sequential PNG export
- ZIP packaging
- Font loading verification

Place `carousel_exporter.py` in the same directory as your HTML file and run:

```bash
python carousel_exporter.py --html carousel.html --output carousel_export.zip
```

Optional flags:
- `--prefix slide` → customize filename prefix
- `--width 1080 --height 1080` → override dimensions
- `--hide-counter` → remove slide counter from exports
- `--quality 95` → PNG compression level (1–100)
