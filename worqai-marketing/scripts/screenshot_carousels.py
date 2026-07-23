#!/usr/bin/env python3
"""Screenshot carousel slides using Playwright."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).parent.parent
OUTPUT = ROOT / "ideation" / "HTMLSFEEDBACK"
OUTPUT.mkdir(parents=True, exist_ok=True)

CAROUSELS = [
    ("production/carousel_ats-te-elimino_cyberpunk.html", "cyberpunk", 5),
    ("production/carousel_0a4-entrevistas_clean-saas.html", "clean-saas", 4),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        for rel_path, name, total_slides in CAROUSELS:
            file_path = ROOT / rel_path
            file_url = f"file:///{file_path.resolve().as_posix()}"
            await page.goto(file_url)
            await page.wait_for_timeout(1000)
            for i in range(total_slides):
                await page.evaluate(f"go({i})")
                await page.wait_for_timeout(600)
                wrap = await page.query_selector("#wrap")
                screenshot_path = OUTPUT / f"{name}_slide{i+1}.png"
                await wrap.screenshot(path=str(screenshot_path), type="png")
                print(f"Saved: {screenshot_path}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
