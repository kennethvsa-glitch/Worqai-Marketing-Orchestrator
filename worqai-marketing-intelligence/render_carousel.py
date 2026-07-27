import os
import asyncio
from playwright.async_api import async_playwright

output_dir = r"C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence\production\wmi\2026-07-25\carousel_05_light"
os.makedirs(output_dir, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 2500, "height": 3000})
        await page.goto(r"file:///C:/Users/kenne/OneDrive/Documentos/manifest-claude-system/projects/worqai-marketing-intelligence/production/wmi/2026-07-25/carousel_05_light.html", wait_until="networkidle")
        
        slides = await page.locator(".slide").all()
        for i, slide in enumerate(slides):
            await slide.screenshot(path=f"{output_dir}\\slide_{i+1:02d}.png")
        await browser.close()

asyncio.run(main())
