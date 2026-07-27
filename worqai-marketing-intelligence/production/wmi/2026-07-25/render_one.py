import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence\production\wmi\2026-07-25")

def render_carousel(playwright, html_name, out_folder_name):
    html_path = BASE_DIR / html_name
    out_dir = BASE_DIR / out_folder_name
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"--- Rendering {html_name} to {out_folder_name} ---")
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)

    file_url = html_path.as_uri()
    page.goto(file_url, wait_until="networkidle")

    slides = page.locator(".slide")
    count = slides.count()
    print(f"Found {count} slides in {html_name}")

    rendered_files = []
    for i in range(count):
        slide = slides.nth(i)
        filename = f"slide_{i+1:02d}.png"
        dest = out_dir / filename
        slide.screenshot(path=str(dest), animations="disabled")
        rendered_files.append(filename)
        print(f"  [+] Saved {filename}")

    # Generate contact sheet HTML
    contact_html_content = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; background: #07080a; padding: 20px; }}
    body {{
      display: grid;
      grid-template-columns: repeat(3, 360px);
      gap: 20px;
      color: #b8ff00;
      font: 700 15px Consolas, monospace;
    }}
    figure {{ margin: 0; }}
    img {{
      display: block;
      width: 360px;
      height: 450px;
      object-fit: cover;
      border: 2px solid #2a3038;
      border-radius: 6px;
    }}
    figcaption {{ padding-top: 8px; text-align: center; }}
  </style>
</head>
<body>
""" + "".join([f'<figure><img src="{f}"><figcaption>SLIDE {idx+1:02d}</figcaption></figure>' for idx, f in enumerate(rendered_files)]) + """
</body>
</html>"""

    contact_html_path = out_dir / "contact-sheet.html"
    contact_html_path.write_text(contact_html_content, encoding="utf-8")

    # Render contact sheet image
    contact_page = browser.new_page(viewport={"width": 1200, "height": 1000}, device_scale_factor=1)
    contact_page.goto(contact_html_path.as_uri(), wait_until="networkidle")
    contact_png_path = out_dir / "contact-sheet.png"
    contact_page.screenshot(path=str(contact_png_path), full_page=True)
    print(f"  [+] Saved contact-sheet.png")

    browser.close()

def main():
    with sync_playwright() as p:
        render_carousel(p, "carousel_01_dark.html", "carousel_01_dark")
    print("\n[SUCCESS] Rendered successfully!")

if __name__ == "__main__":
    main()
