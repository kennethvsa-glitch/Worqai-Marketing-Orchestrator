import asyncio
from playwright.async_api import async_playwright
import os

HTML_PATH = r"C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence\production\wmi\2026-07-25\carousel_04_light.html"
OUTPUT_DIR = r"C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence\production\wmi\2026-07-25\carousel_04_light"

async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(device_scale_factor=2)
        await page.goto(f"file:///{HTML_PATH.replace(chr(92), '/')}")
        
        # Wait a bit for fonts and SVG
        await page.wait_for_timeout(1000)
        
        slides = await page.query_selector_all('.slide')
        for i, slide in enumerate(slides):
            out_path = os.path.join(OUTPUT_DIR, f"slide_{i+1:02d}.png")
            await slide.screenshot(path=out_path)
            print(f"Rendered: {out_path}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
