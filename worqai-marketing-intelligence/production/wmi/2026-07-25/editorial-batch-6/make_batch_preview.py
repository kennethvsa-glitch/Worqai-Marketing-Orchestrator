"""Build a single visual index from the six verified contact sheets."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
ITEMS = [
    ("01", "CAMBIO DE CARRERA", "01-career-change"),
    ("02", "EDITAR ES ESTRATEGIA", "02-editing"),
    ("03", "PAUSA LABORAL", "03-career-gap"),
    ("04", "EVIDENCIA JUNIOR", "04-junior-evidence"),
    ("05", "CRITERIO SENIOR", "05-senior-criterion"),
    ("06", "LA VACANTE ES EL MAPA", "06-vacancy-strategy"),
]

W, H = 1660, 1790
CELL_W, IMAGE_H = 770, 510
BG, PAPER, LIME = "#080807", "#F1EDE3", "#B8FF00"

canvas = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(canvas)
font_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 28)
font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)

draw.text((60, 35), "WORQAI / 6 CAROUSELS EDITORIALES", fill=PAPER, font=font_bold)
draw.text((60, 76), "42 slides · 1080 × 1350 · dark editorial systems", fill=LIME, font=font_small)

for index, (number, title, folder) in enumerate(ITEMS):
    col, row = index % 2, index // 2
    x, y = 60 + col * 800, 130 + row * 545
    source = Image.open(ROOT / folder / "final" / "contact-sheet.png").convert("RGB")
    source = source.resize((CELL_W, IMAGE_H), Image.Resampling.LANCZOS)
    canvas.paste(source, (x, y + 36))
    draw.text((x, y), f"{number}  {title}", fill=PAPER, font=font_bold)

canvas.save(ROOT / "batch-preview.png", quality=95)

