import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    html_path = r"C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence\production\wmi\2026-07-25\carousel_03_dark.html"
    out_dir = r"C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence\production\wmi\2026-07-25\carousel_03_dark"
    
    os.makedirs(out_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350 * 6 + 200})
        await page.goto(f"file:///{html_path.replace(chr(92), '/')}")
        
        for i in range(1, 7):
            slide = await page.query_selector(f"#slide-{i}")
            if slide:
                await slide.screenshot(path=os.path.join(out_dir, f"slide_{i}.png"))
                
        await browser.close()
        print(f"Screenshots saved to {out_dir}")

if __name__ == "__main__":
    asyncio.run(main())
