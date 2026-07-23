
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
            const demoStyle = demoGroup ? window.getComputedStyle(demoGroup) : null;
            const safeBottom = window.innerHeight - 200;
            const safeRight = window.innerWidth - 56;
            const safeLeft = 56;
            const safeTop = 120;
            const overflows = [];
            document.querySelectorAll('[data-copy]').forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.width === 0 && r.height === 0) return;
                if (r.bottom > safeBottom || r.right > safeRight || r.left < safeLeft || r.top < safeTop) {
                    overflows.push(el.dataset.copy);
                }
            });
            return {
                demoGroup: {
                    top: demoStyle ? demoStyle.top : null,
                    position: demoStyle ? demoStyle.position : null,
                },
                safeBottom, safeTop,
                overflowCount: overflows.length,
                overflows: overflows.slice(0, 10)
            };
        }
    """)
    print(json.dumps(result, indent=2))
    browser.close()
