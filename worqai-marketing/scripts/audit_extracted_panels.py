from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path.cwd()
OUT = ROOT / "production" / "_review_recent" / "_panel_audit"
OUT.mkdir(parents=True, exist_ok=True)

BG_IDS = [
    "digital-glass-full",
    "satin-waves-full",
    "glass-panel-full",
    "cosmic-ribbons",
    "energy-flow-full",
    "pastel-waves",
    "geo-blue-grid",
    "galactic-dream-full",
    "glowing-energy-flow",
    "oceanic-wave",
]

def label_image(img: Image.Image, text: str) -> Image.Image:
    w, h = img.size
    canvas = Image.new("RGB", (w, h + 42), "#151515")
    canvas.paste(img.convert("RGB"), (0, 42))
    d = ImageDraw.Draw(canvas)
    d.text((12, 13), text, fill="#ffffff")
    return canvas

def make_sheet(bg_id: str):
    bg_dir = ROOT / "brand" / "generated-bg" / bg_id
    panel_dirs = sorted([p for p in bg_dir.glob("panel_*") if p.is_dir()])
    items = []
    for p in panel_dirs:
        img_path = p / "original.png"
        if not img_path.exists():
            # Fall back to first png in panel dir.
            pngs = sorted(p.glob("*.png"))
            if not pngs:
                continue
            img_path = pngs[0]
        img = Image.open(img_path).resize((260, 260), Image.LANCZOS)
        items.append(label_image(img, p.name))

    if not items:
        return

    cols = 4
    rows = (len(items) + cols - 1) // cols
    gap = 18
    title_h = 44
    cell_w, cell_h = items[0].size
    sheet = Image.new("RGB", (cols * cell_w + (cols + 1) * gap, title_h + rows * cell_h + (rows + 1) * gap), "#101010")
    d = ImageDraw.Draw(sheet)
    d.text((18, 16), bg_id, fill="#ffffff")
    for i, item in enumerate(items):
        x = gap + (i % cols) * (cell_w + gap)
        y = title_h + gap + (i // cols) * (cell_h + gap)
        sheet.paste(item, (x, y))
    out = OUT / f"{bg_id}_panels.png"
    sheet.save(out)
    print(out)

for bg_id in BG_IDS:
    make_sheet(bg_id)
