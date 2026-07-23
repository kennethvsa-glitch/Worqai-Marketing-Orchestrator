
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1920})
    page.goto("file:///C:/Users/kenne/motion-studio/templates/scenes/scene-launch-villain-v4.html")
    page.wait_for_timeout(500)  # Wait for scripts to run
    
    # Run the overflow check
    result = page.evaluate("""
        () => {
            const safeBottom = window.innerHeight - 200;
            const safeRight = window.innerWidth - 56;
            const safeLeft = 56;
            const safeTop = 120;
            const overflows = [];
            document.querySelectorAll('[data-copy]').forEach(el => {
                const r = el.getBoundingClientRect();
                if (r.width === 0 && r.height === 0) return;
                if (r.bottom > safeBottom || r.right > safeRight || r.left < safeLeft || r.top < safeTop) {
                    overflows.push({
                        copy: el.dataset.copy,
                        top: r.top, bottom: r.bottom, left: r.left, right: r.right,
                        width: r.width, height: r.height,
                        parent: el.parentElement ? el.parentElement.id || el.parentElement.className : 'none'
                    });
                }
            });
            return {
                innerHeight: window.innerHeight,
                innerWidth: window.innerWidth,
                safeBottom, safeRight, safeLeft, safeTop,
                overflows
            };
        }
    """)
    print(json.dumps(result, indent=2))
    browser.close()
