
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1920})
    page.goto("file:///C:/Users/kenne/motion-studio/templates/scenes/scene-launch-villain-v4.html")
    page.wait_for_timeout(500)
    
    result = page.evaluate("""
        () => {
            const demoGroup = document.getElementById('demo-group');
            const bannerArea = document.getElementById('banner-area');
            const bannerGeneric = document.getElementById('banner-generic');
            const head = document.getElementById('banner-generic-head');
            const demoStyle = demoGroup ? window.getComputedStyle(demoGroup) : null;
            
            return {
                demoGroup: demoGroup ? {
                    rect: demoGroup.getBoundingClientRect(),
                    top: demoStyle ? demoStyle.top : null,
                    position: demoStyle ? demoStyle.position : null,
                } : null,
                bannerArea: bannerArea ? bannerArea.getBoundingClientRect() : null,
                bannerGeneric: bannerGeneric ? bannerGeneric.getBoundingClientRect() : null,
                head: head ? head.getBoundingClientRect() : null,
            };
        }
    """)
    print(json.dumps(result, indent=2))
    browser.close()
