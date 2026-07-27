#!/usr/bin/env python3
"""Render all 6 carousel HTML files to individual slide PNGs."""
import asyncio
import pathlib
from playwright.async_api import async_playwright

BASE = pathlib.Path(r"C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence\production\wmi\2026-07-25")

CAROUSELS = [
    ("carousel_01_dark.html", "carousel_01_dark"),
    ("carousel_02_dark.html", "carousel_02_dark"),
    ("carousel_03_dark.html", "carousel_03_dark"),
    ("carousel_04_light.html", "carousel_04_light"),
    ("carousel_05_light.html", "carousel_05_light"),
    ("carousel_06_light.html", "carousel_06_light"),
]

SLIDE_W, SLIDE_H = 1080, 1350


async def render_carousel(html_file: pathlib.Path, out_dir: pathlib.Path, browser):
    if not html_file.exists():
        print(f"  SKIP {html_file.name} (not found)")
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    page = await browser.new_page(viewport={"width": SLIDE_W, "height": SLIDE_H})
    await page.goto(html_file.as_uri())
    await page.wait_for_timeout(1500)

    slides = await page.query_selector_all(".slide, [class*='slide']")
    if not slides:
        # Try alternative selectors
        slides = await page.query_selector_all("section, div[id^='slide']")
    
    if not slides:
        print(f"  WARNING: No slides found in {html_file.name}")
        await page.close()
        return

    print(f"  Found {len(slides)} slides in {html_file.name}")
    for i, slide in enumerate(slides, 1):
        path = out_dir / f"slide_{i:02d}.png"
        await slide.screenshot(path=str(path))
        print(f"    -> {path.name}")

    await page.close()


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for html_name, dir_name in CAROUSELS:
            html_path = BASE / html_name
            out_path = BASE / dir_name
            print(f"\nRendering {html_name}...")
            await render_carousel(html_path, out_path, browser)
        await browser.close()
    print("\nAll carousels rendered.")


if __name__ == "__main__":
    asyncio.run(main())
