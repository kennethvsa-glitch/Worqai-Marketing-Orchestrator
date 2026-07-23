#!/usr/bin/env python3
"""
carousel_exporter.py
WorqAI — Carousel to ZIP Exporter
Companion script for carousel-to-zip-exporter skill

Usage:
    python carousel_exporter.py --html carousel.html
    python carousel_exporter.py --input production/carousel.html --output export/
    python carousel_exporter.py --html carousel.html --output my_carousel.zip
    python carousel_exporter.py --html carousel.html --prefix post_cv --width 1080 --height 1350
    python carousel_exporter.py --html carousel.html --hide-counter --quality 95
    python carousel_exporter.py --html carousel.html --no-contact-sheet

Requirements:
    pip install playwright pillow
    playwright install chromium
"""

import argparse
import asyncio
import os
import sys
import zipfile
import tempfile
import re
from pathlib import Path


# ─────────────────────────────────────────────
# AUTO-INSTALL DEPENDENCIES
# ─────────────────────────────────────────────

def install_dependencies():
    import subprocess
    packages = ["playwright", "pillow"]
    for pkg in packages:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            print(f"[setup] Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch()
    except Exception:
        print("[setup] Installing Playwright Chromium browser...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])

install_dependencies()


# ─────────────────────────────────────────────
# SLIDE DETECTOR
# ─────────────────────────────────────────────

def detect_slide_count(html_path: str) -> tuple[int, str]:
    """
    Parse HTML and detect slide count + CSS selector.
    Returns (count, selector).
    Checks common selectors used by ad-creative-generator HTML output.
    """
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Priority order: most specific first
    selectors = [
        (r'class=["\']slide["\' ]', ".slide"),
        (r'class=["\'][^"\']*carousel-item[^"\']*["\']>', ".carousel-item"),
        (r'class=["\'][^"\']*swiper-slide[^"\']*["\']>', ".swiper-slide"),
        (r'data-slide=', "[data-slide]"),
        (r'class=["\'][^"\']*panel[^"\']*["\']>', ".panel"),
    ]

    for pattern, selector in selectors:
        matches = re.findall(pattern, content)
        if matches:
            print(f"[detect] Found {len(matches)} slides using selector: {selector}")
            return len(matches), selector

    # Fallback: count divs with id="slide-N"
    fallback = re.findall(r'id=["\']slide-\d+["\']>', content)
    if fallback:
        print(f"[detect] Found {len(fallback)} slides using id=slide-N pattern")
        return len(fallback), "[id^='slide-']"

    raise ValueError(
        "Could not detect slides in HTML. "
        "Make sure slides use class='slide', class='carousel-item', or data-slide attribute. "
        "See carousel-to-zip-exporter.md for details."
    )


# ─────────────────────────────────────────────
# ASYNC RENDERER
# ─────────────────────────────────────────────

async def render_slides(
    html_path: str,
    output_dir: str,
    selector: str,
    slide_count: int,
    width: int,
    height: int,
    prefix: str,
    hide_counter: bool,
    quality: int,
) -> list[str]:
    """
    Launch headless Chromium, render each slide, screenshot to PNG.
    Returns list of successfully exported file paths.
    """
    from playwright.async_api import async_playwright

    abs_path = Path(html_path).resolve()
    file_url = abs_path.as_uri()

    exported = []
    failed = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-setuid-sandbox"])
        context = await browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=1,
        )
        page = await context.new_page()

        print(f"[render] Loading: {file_url}")
        await page.goto(file_url, wait_until="networkidle", timeout=30000)

        # Wait for fonts to load
        await page.wait_for_timeout(1500)

        # Remove preview-scaling transforms that carousels apply for browser preview.
        # .preview-cage often has transform:scale(0.5) and height:540px so the 1080px
        # slide fits on a laptop screen. Playwright element.screenshot() respects ancestor
        # transforms, so without this the screenshot comes out at 540×540 not 1080×1080.
        await page.add_style_tag(content="""
            body, .preview-cage, .preview-wrap, .preview-container {
                margin: 0 !important;
                padding: 0 !important;
            }
            .preview-cage, .preview-wrap, .preview-container {
                transform: none !important;
                height: auto !important;
                width: 100% !important;
                max-width: none !important;
            }
            .viewer, .viewer-wrap {
                transform: none !important;
                width: """ + str(width) + """px !important;
                max-width: """ + str(width) + """px !important;
            }
            .wrap {
                width: """ + str(width) + """px !important;
                height: """ + str(height) + """px !important;
                aspect-ratio: auto !important;
            }
            .slide {
                width: """ + str(width) + """px !important;
                min-width: """ + str(width) + """px !important;
                height: """ + str(height) + """px !important;
            }
        """)
        # Also strip any inline transform:scale and force dimensions
        await page.evaluate(f"""
            document.querySelectorAll('body, .preview-cage, .preview-wrap, .preview-container').forEach(el => {{
                el.style.transform = 'none';
                el.style.margin = '0';
                el.style.padding = '0';
                el.style.height = 'auto';
                el.style.width = '100%';
                el.style.maxWidth = 'none';
            }});
            document.querySelectorAll('.viewer, .viewer-wrap').forEach(el => {{
                el.style.transform = 'none';
                el.style.width = '{width}px';
                el.style.maxWidth = '{width}px';
            }});
            document.querySelectorAll('.wrap').forEach(el => {{
                el.style.width = '{width}px';
                el.style.height = '{height}px';
                el.style.aspectRatio = 'auto';
            }});
            document.querySelectorAll('.slide').forEach(el => {{
                el.style.width = '{width}px';
                el.style.minWidth = '{width}px';
                el.style.height = '{height}px';
            }});
        """)
        await page.wait_for_timeout(100)

        # Fast-forward all CSS animations to their completed state.
        # Negative animation-delay seeks past the duration; paused freezes there.
        # This fixes typewriter (width:0→100%), donut draw, waffle pop, bar fills,
        # check draws, fadein stagger — anything with animation-fill-mode: forwards/both.
        # Infinite decorative animations (bars, ticker, grid) land at a natural mid-point.
        await page.add_style_tag(content="""
            *, *::before, *::after {
                animation-play-state: paused !important;
                animation-delay: -10s !important;
                transition-duration: 0ms !important;
                transition-delay: 0ms !important;
            }
        """)
        await page.wait_for_timeout(150)

        # Inject helper JS to expose and control slides
        await page.evaluate(f"""
            window._EXPORT_SELECTOR = '{selector}';
            window._EXPORT_TOTAL = {slide_count};

            window.showSlide = function(index) {{
                const slides = document.querySelectorAll(window._EXPORT_SELECTOR);
                slides.forEach((s, i) => {{
                    s.style.display = i === index ? 'flex' : 'none';
                    s.style.visibility = i === index ? 'visible' : 'hidden';
                    s.style.opacity = i === index ? '1' : '0';
                    s.style.position = i === index ? 'relative' : 'absolute';
                }});
            }};

            // Hide all navigation chrome
            const navSelectors = [
                '.nav-btn', '.nav-arrow', '.arrow', '[class*="arrow"]',
                '[class*="nav"]', '[class*="swipe"]', '.prev', '.next',
                'button[aria-label]', '.carousel-control'
            ];
            navSelectors.forEach(sel => {{
                document.querySelectorAll(sel).forEach(el => {{
                    el.style.display = 'none';
                }});
            }});
        """)

        if hide_counter:
            await page.evaluate("""
                const counterSelectors = ['.counter', '.slide-counter', '[class*="counter"]', '[class*="progress"]'];
                counterSelectors.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => { el.style.display = 'none'; });
                });
            """)

        # Export each slide
        pad = 2 if slide_count <= 99 else 3

        for i in range(slide_count):
            slide_num = str(i + 1).zfill(pad)
            filename = f"{prefix}_{slide_num}.png"
            output_path = os.path.join(output_dir, filename)

            try:
                await page.evaluate(f"window.showSlide({i})")
                await page.wait_for_timeout(300)

                # Screenshot the container (first matching slide element)
                element = page.locator(selector).nth(i)
                await element.screenshot(path=output_path, type="png")

                # Verify non-empty
                size = os.path.getsize(output_path)
                if size < 500:
                    raise ValueError(f"Screenshot too small ({size} bytes) — likely blank")

                exported.append(output_path)
                print(f"[export] Slide {slide_num} -> {filename} ({size // 1024}KB)")

            except Exception as e:
                print(f"[ERROR] Slide {slide_num} failed: {e}")
                failed.append(slide_num)

        await browser.close()

    if failed:
        print(f"\n[WARNING] Failed slides: {', '.join(failed)}")
    else:
        print(f"\n[done] All {len(exported)} slides exported successfully.")

    return exported


# ─────────────────────────────────────────────
# ZIP PACKAGER
# ─────────────────────────────────────────────

def package_zip(image_paths: list[str], zip_path: str):
    """
    Creates a flat ZIP with all PNG files. No subfolders.
    """
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for img_path in sorted(image_paths):
            arcname = os.path.basename(img_path)
            zf.write(img_path, arcname)
            print(f"[zip] Added: {arcname}")

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"\n[zip] Created: {zip_path} ({size_mb:.2f} MB, {len(image_paths)} files)")


# ─────────────────────────────────────────────
# CONTACT SHEET GENERATOR
# ─────────────────────────────────────────────

def build_contact_sheet(
    image_paths: list,
    output_path: str,
    carousel_name: str = "",
    thumb_size: int = 360,
    cols: int = 0,
) -> str:
    """Generate a contact sheet PNG showing all slides as thumbnails.

    Dark-background grid with slide numbers. Saved next to the ZIP.
    Used for visual QA before posting — see all slides in one glance.

    Args:
        image_paths: Ordered list of PNG slide paths.
        output_path: Full path for the contact sheet PNG.
        carousel_name: Label displayed at the top of the sheet.
        thumb_size: Thumbnail edge size in pixels (slides are square).
        cols: Grid columns (0 = auto: ≤8 slides → 4 cols, else 5 cols).

    Returns: output_path on success, empty string on failure.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        import math
    except ImportError:
        print("[sheet] Pillow not available — skipping contact sheet.")
        return ""

    if not image_paths:
        return ""

    n = len(image_paths)

    # Auto-layout
    if cols <= 0:
        cols = min(4, n) if n <= 8 else min(5, n)
    rows = math.ceil(n / cols)

    BG      = (10, 10, 14)      # near-black
    CARD_BG = (20, 20, 26)      # slightly lighter for thumbnails
    BORDER  = (36, 36, 46)      # subtle thumbnail border
    TEXT_LO = (110, 110, 125)   # muted text (slide numbers)
    TEXT_HI = (210, 210, 220)   # header label
    ACCENT  = (78, 205, 196)    # teal accent strip

    PAD      = 14   # gap between thumbnails
    TOP_PAD  = 58   # header bar height
    BOT_PAD  = 28   # bottom margin
    LABEL_H  = 26   # height below thumbnail for slide number

    total_w = cols * (thumb_size + PAD) + PAD
    total_h = TOP_PAD + rows * (thumb_size + LABEL_H + PAD) + BOT_PAD

    sheet = Image.new("RGB", (total_w, total_h), BG)
    draw  = ImageDraw.Draw(sheet)

    # ── Load fonts (graceful fallback) ──────────────────────────────────────
    font_hdr   = ImageFont.load_default()
    font_label = ImageFont.load_default()
    for font_name in ("arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf", "arial.ttf"):
        try:
            font_hdr = ImageFont.truetype(font_name, 16)
            break
        except Exception:
            pass
    for font_name in ("arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"):
        try:
            font_label = ImageFont.truetype(font_name, 13)
            break
        except Exception:
            pass

    # ── Header bar ──────────────────────────────────────────────────────────
    # Accent strip on left edge
    draw.rectangle([(0, 0), (3, TOP_PAD)], fill=ACCENT)
    # Carousel name
    label_y = (TOP_PAD - 18) // 2
    if carousel_name:
        draw.text((PAD + 8, label_y), carousel_name, fill=TEXT_HI, font=font_hdr)
    # Slide count badge (right side)
    badge = f"{n} slides"
    draw.text((total_w - PAD - 68, label_y), badge, fill=TEXT_LO, font=font_label)
    # Separator line
    draw.line([(4, TOP_PAD - 1), (total_w, TOP_PAD - 1)], fill=BORDER, width=1)

    # ── Thumbnails ──────────────────────────────────────────────────────────
    for idx, img_path in enumerate(sorted(image_paths)):
        row = idx // cols
        col = idx % cols
        x = PAD + col * (thumb_size + PAD)
        y = TOP_PAD + row * (thumb_size + LABEL_H + PAD)

        # Card background
        draw.rectangle(
            [(x - 2, y - 2), (x + thumb_size + 2, y + thumb_size + 2)],
            fill=CARD_BG, outline=BORDER, width=1
        )

        try:
            img = Image.open(img_path).convert("RGB")
            img.thumbnail((thumb_size, thumb_size), Image.LANCZOS)
            # Center in cell
            tx = x + (thumb_size - img.width) // 2
            ty = y + (thumb_size - img.height) // 2
            sheet.paste(img, (tx, ty))
        except Exception as e:
            draw.rectangle([x, y, x + thumb_size, y + thumb_size], fill=(30, 18, 18))
            draw.text((x + 8, y + thumb_size // 2 - 8), f"error: {e}", fill=(200, 60, 60), font=font_label)

        # Slide number
        num_label = f"{idx + 1:02d}"
        # Center the label under the thumbnail
        try:
            bbox = draw.textbbox((0, 0), num_label, font=font_label)
            lw = bbox[2] - bbox[0]
        except AttributeError:
            lw = len(num_label) * 8
        lx = x + (thumb_size - lw) // 2
        ly = y + thumb_size + 6
        draw.text((lx, ly), num_label, fill=TEXT_LO, font=font_label)

    sheet.save(output_path, "PNG", optimize=True)
    size_kb = os.path.getsize(output_path) // 1024
    print(f"[sheet] Contact sheet -> {Path(output_path).name} ({size_kb} KB, {cols}x{rows} grid)")
    return output_path


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Export HTML carousel slides to numbered PNGs + ZIP + contact sheet.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python carousel_exporter.py --html carousel.html
  python carousel_exporter.py --input production/carousel.html --output export/
  python carousel_exporter.py --html carousel.html --output cv_post.zip --prefix slide
  python carousel_exporter.py --html carousel.html --width 1080 --height 1350
  python carousel_exporter.py --html carousel.html --hide-counter --no-contact-sheet
        """
    )
    # --input is the canonical flag (CLAUDE.md convention); --html kept for compat
    parser.add_argument("--input",  dest="html", default=None, help="Path to HTML carousel file (alias for --html)")
    parser.add_argument("--html",   dest="html", default=None, help="Path to HTML carousel file")
    parser.add_argument("--output", default=None,
                        help="Output ZIP path or output directory. Default: export/ directory next to HTML.")
    parser.add_argument("--prefix", default="slide", help="PNG filename prefix (default: slide → slide_01.png)")
    parser.add_argument("--width",  type=int, default=1080, help="Viewport width in pixels (default: 1080)")
    parser.add_argument("--height", type=int, default=1080, help="Viewport height in pixels (default: 1080)")
    parser.add_argument("--hide-counter", action="store_true", help="Hide slide counter element from exports")
    parser.add_argument("--quality", type=int, default=95, help="PNG quality 1-100 (default: 95)")
    parser.add_argument("--no-contact-sheet", action="store_true",
                        help="Skip generating the contact sheet PNG after export")

    args = parser.parse_args()

    if not args.html:
        parser.error("Provide --input or --html with the path to the carousel HTML file.")

    # Validate HTML path
    if not os.path.exists(args.html):
        print(f"[ERROR] HTML file not found: {args.html}")
        sys.exit(1)

    html_stem = Path(args.html).stem  # e.g. "carousel_rrhh-no-dice-filtro_s01"

    # Resolve output ZIP path
    if args.output is None:
        # Default: export/ next to this script's project root
        out_dir = Path(args.html).parent.parent / "export"
        out_dir.mkdir(parents=True, exist_ok=True)
        zip_path = str(out_dir / f"{html_stem}.zip")
    elif os.path.isdir(args.output) or args.output.endswith("/") or args.output.endswith("\\"):
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        zip_path = str(out_dir / f"{html_stem}.zip")
    else:
        zip_path = args.output
        out_dir = Path(zip_path).parent

    contact_sheet_path = str(out_dir / f"{html_stem}_contact_sheet.png")

    print("=" * 56)
    print("  WorqAI Carousel Exporter")
    print("=" * 56)
    print(f"  HTML:          {args.html}")
    print(f"  Output ZIP:    {zip_path}")
    print(f"  Contact sheet: {'skipped' if args.no_contact_sheet else contact_sheet_path}")
    print(f"  Dimensions:    {args.width}×{args.height}px")
    print(f"  Counter:       {'hidden' if args.hide_counter else 'visible'}")
    print("=" * 56 + "\n")

    # Detect slides
    slide_count, selector = detect_slide_count(args.html)
    print(f"[info] Slide count: {slide_count}\n")

    # Create temp dir for PNGs
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Render slides
        exported = asyncio.run(render_slides(
            html_path=args.html,
            output_dir=tmp_dir,
            selector=selector,
            slide_count=slide_count,
            width=args.width,
            height=args.height,
            prefix=args.prefix,
            hide_counter=args.hide_counter,
            quality=args.quality,
        ))

        if not exported:
            print("[ERROR] No slides were exported. Check your HTML file and try again.")
            sys.exit(1)

        # Package ZIP
        package_zip(exported, zip_path)

        # Generate contact sheet while PNGs are still in temp dir
        if not args.no_contact_sheet:
            build_contact_sheet(
                image_paths=sorted(exported),
                output_path=contact_sheet_path,
                carousel_name=html_stem,
            )

    print(f"\n[done] Export complete.")
    print(f"  ZIP:           {zip_path}")
    if not args.no_contact_sheet and os.path.exists(contact_sheet_path):
        print(f"  Contact sheet: {contact_sheet_path}")
    print(f"  Slides:        {len(exported)}\n")
    print("  Upload the numbered PNGs directly to Instagram or Facebook as a carousel post.")


if __name__ == "__main__":
    main()
