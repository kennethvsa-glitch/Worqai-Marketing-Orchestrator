import asyncio
from playwright.async_api import async_playwright
import os

HTML_FILE = r"C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence\production\wmi\2026-07-25\carousel_02_dark.html"
OUT_DIR = r"C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence\production\wmi\2026-07-25\carousel_02_dark"

async def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350 * 6 + 200})
        await page.goto(f"file:///{HTML_FILE}")
        
        # Wait a bit for fonts and rendering
        await page.wait_for_timeout(2000)
        
        slides = await page.query_selector_all('.slide')
        for i, slide in enumerate(slides):
            await slide.screenshot(path=os.path.join(OUT_DIR, f"slide_{i+1:02d}.png"))
            print(f"Rendered slide {i+1}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
