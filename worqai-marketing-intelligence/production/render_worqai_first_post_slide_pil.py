from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
FONT_ROOT = Path(r"C:\Users\kenne\OneDrive\Documentos\cv-tailored\fonts")
OUT_2X = ROOT / "worqai-linkedin-first-post-slide@2x.png"
OUT_1X = ROOT / "worqai-linkedin-first-post-slide.png"

SCALE = 2
W = H = 1080 * SCALE

LIME = (192, 240, 48, 255)
WHITE = (255, 255, 255, 255)
OFF_WHITE = (230, 234, 224, 255)
MUTED = (164, 170, 158, 255)
BLACK = (5, 6, 5, 255)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    paths = {
        "lato-bold": FONT_ROOT / "Lato" / "Lato-Bold.ttf",
        "lato-regular": FONT_ROOT / "Lato" / "Lato-Regular.ttf",
        "mono": FONT_ROOT / "JetBrains-Mono" / "JetBrainsMono-VariableFont_wght.ttf",
    }
    return ImageFont.truetype(str(paths[name]), size * SCALE)


F_HEAD = font("lato-bold", 88)
F_HEAD_SMALL = font("lato-bold", 82)
F_BODY = font("lato-regular", 29)
F_BODY_BOLD = font("lato-bold", 29)
F_KICKER = font("mono", 18)
F_PILL = font("mono", 13)
F_BRAND = font("lato-bold", 31)
F_CTA = font("lato-bold", 17)
F_SCORE = font("lato-bold", 74)
F_SCORE_SMALL = font("lato-bold", 34)
F_DEVICE_TITLE = font("lato-bold", 25)
F_DEVICE_TEXT = font("lato-bold", 15)
F_TEMPLATE = font("lato-bold", 22)


def sx(value: float) -> int:
    return round(value * SCALE)


def rgba(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return (*color, round(255 * alpha))


def make_background() -> Image.Image:
    img = Image.new("RGBA", (W, H), BLACK)
    px = img.load()
    c1 = (21, 24, 17)
    c2 = (5, 5, 5)
    c3 = (11, 12, 11)
    for y in range(H):
        yn = y / (H - 1)
        for x in range(W):
            xn = x / (W - 1)
            t = min(1, max(0, (xn * 0.62 + yn * 0.58)))
            base = tuple(round(c1[i] * (1 - t) + c2[i] * t) for i in range(3))
            shadow = tuple(round(base[i] * 0.82 + c3[i] * 0.18) for i in range(3))
            px[x, y] = (*shadow, 255)
    return img


def add_radial(img: Image.Image, center: tuple[int, int], radius: int, color: tuple[int, int, int], alpha: float) -> None:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    opx = overlay.load()
    cx, cy = center
    r2 = radius * radius
    for y in range(max(0, cy - radius), min(H, cy + radius)):
        for x in range(max(0, cx - radius), min(W, cx + radius)):
            d2 = (x - cx) ** 2 + (y - cy) ** 2
            if d2 < r2:
                d = math.sqrt(d2) / radius
                a = alpha * (1 - d) ** 1.9
                if a > 0.002:
                    opx[x, y] = (*color, round(255 * a))
    img.alpha_composite(overlay)


def draw_text_runs(draw: ImageDraw.ImageDraw, xy: tuple[int, int], runs: list[tuple[str, ImageFont.FreeTypeFont, tuple[int, int, int, int]]], line_gap: int = 0) -> tuple[int, int]:
    x, y = xy
    start_x = x
    max_x = x
    for text, fnt, color in runs:
        pieces = text.split("\n")
        for i, piece in enumerate(pieces):
            if piece:
                draw.text((x, y), piece, font=fnt, fill=color)
                bbox = draw.textbbox((x, y), piece, font=fnt)
                x = bbox[2]
                max_x = max(max_x, x)
            if i != len(pieces) - 1:
                y += fnt.size + line_gap
                x = start_x
    return max_x, y


def wrap_words(text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    for word in text.split():
        candidate = f"{current} {word}".strip()
        width = probe.textbbox((0, 0), candidate, font=fnt)[2]
        if width <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def rounded_rect(layer: Image.Image, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1) -> None:
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_device() -> Image.Image:
    device_w, device_h = sx(398), sx(650)
    pad = sx(22)
    device = Image.new("RGBA", (device_w + sx(40), device_h + sx(40)), (0, 0, 0, 0))
    d = ImageDraw.Draw(device)
    outer = (sx(20), sx(20), sx(20) + device_w, sx(20) + device_h)

    d.rounded_rectangle(outer, radius=sx(34), fill=(10, 12, 10, 246), outline=(255, 255, 255, 42), width=sx(1))
    d.rounded_rectangle((outer[0] - sx(16), outer[1] - sx(16), outer[2] + sx(16), outer[3] + sx(16)), radius=sx(44), outline=rgba((192, 240, 48), 0.16), width=sx(1))

    screen = (outer[0] + pad, outer[1] + pad, outer[2] - pad, outer[3] - pad)
    d.rounded_rectangle(screen, radius=sx(24), fill=(238, 242, 234, 255), outline=(0, 0, 0, 26), width=sx(1))

    x0, y0 = screen[0] + sx(22), screen[1] + sx(22)
    d.text((x0, y0), "CV SCORE", font=F_PILL, fill=(16, 19, 16, 138))
    d.text((screen[2] - sx(166), y0 + sx(2)), "84", font=F_SCORE, fill=(16, 19, 16, 255))
    d.text((screen[2] - sx(58), y0 + sx(36)), "/100", font=F_SCORE_SMALL, fill=(141, 183, 0, 255))

    y = y0 + sx(112)
    d.text((x0, y), "Tu CV antes\nde postular", font=F_DEVICE_TITLE, fill=(16, 19, 16, 255), spacing=sx(1))
    y += sx(84)
    for pct in (0.84, 0.72, 0.91):
        d.rounded_rectangle((x0, y, screen[2] - sx(22), y + sx(11)), radius=sx(8), fill=(16, 19, 16, 28))
        d.rounded_rectangle((x0, y, x0 + round((screen[2] - sx(22) - x0) * pct), y + sx(11)), radius=sx(8), fill=LIME)
        y += sx(24)

    y += sx(20)
    checks = [
        "Resumen más claro para el puesto",
        "Keywords alineadas a la vacante",
        "Formato fácil de leer por ATS",
        "Experiencia real, mejor explicada",
    ]
    for item in checks:
        d.line((x0, y, screen[2] - sx(22), y), fill=(16, 19, 16, 28), width=sx(1))
        y += sx(13)
        d.rounded_rectangle((x0, y, x0 + sx(24), y + sx(24)), radius=sx(8), fill=(16, 19, 16, 255))
        d.line(
            (x0 + sx(6), y + sx(13), x0 + sx(10), y + sx(18), x0 + sx(18), y + sx(7)),
            fill=LIME,
            width=sx(3),
            joint="curve",
        )
        line_x = x0 + sx(36)
        for line in wrap_words(item, F_DEVICE_TEXT, screen[2] - sx(24) - line_x):
            d.text((line_x, y - sx(1)), line, font=F_DEVICE_TEXT, fill=(16, 19, 16, 245))
            y += sx(19)
        y += sx(12)

    template = Image.new("RGBA", (sx(210), sx(118)), (0, 0, 0, 0))
    td = ImageDraw.Draw(template)
    td.rounded_rectangle((0, 0, sx(210), sx(118)), radius=sx(18), fill=(9, 10, 9, 242), outline=rgba((192, 240, 48), 0.34), width=sx(1))
    td.text((sx(16), sx(15)), "TAILORING", font=F_PILL, fill=LIME)
    td.text((sx(16), sx(42)), "Adaptado a\nla vacante", font=F_TEMPLATE, fill=WHITE, spacing=sx(2))
    template = template.rotate(-5.5, resample=Image.Resampling.BICUBIC, expand=True)
    device.alpha_composite(template, (sx(-14), device_h - sx(68)))

    return device.rotate(2.5, resample=Image.Resampling.BICUBIC, expand=True)


def main() -> None:
    img = make_background()
    add_radial(img, (sx(928), sx(125)), sx(390), (192, 240, 48), 0.22)
    add_radial(img, (sx(215), sx(388)), sx(365), (192, 240, 48), 0.1)

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Structural accents from the approved carousel style.
    d.rectangle((0, 0, sx(6), H), fill=rgba((192, 240, 48), 0.68))
    for x in range(0, W, sx(72)):
        d.line((x, 0, x, H), fill=rgba((192, 240, 48), 0.055), width=sx(1))
    for y in range(0, H, sx(72)):
        d.line((0, y, W, y), fill=rgba((192, 240, 48), 0.045), width=sx(1))
    d.line((sx(282), 0, sx(515), H), fill=rgba((192, 240, 48), 0.105), width=sx(78))
    d.line((sx(850), 0, sx(588), sx(730)), fill=rgba((255, 255, 255), 0.045), width=sx(94))
    d.ellipse((sx(770), sx(-110), sx(1390), sx(510)), outline=rgba((192, 240, 48), 0.22), width=sx(1))

    watermark_font = font("lato-bold", 930)
    d.text((sx(-70), sx(-256)), "W", font=watermark_font, fill=rgba((192, 240, 48), 0.052))

    # Topline.
    d.text((sx(64), sx(72)), "WORQAI · CV INTELLIGENCE", font=F_KICKER, fill=LIME)
    badge = (sx(763), sx(60), sx(1016), sx(102))
    d.rounded_rectangle(badge, radius=sx(22), fill=rgba((192, 240, 48), 0.1), outline=rgba((192, 240, 48), 0.52), width=sx(1))
    d.ellipse((sx(783), sx(76), sx(791), sx(84)), fill=LIME)
    d.text((sx(804), sx(74)), "HECHO EN COSTA RICA", font=F_PILL, fill=(234, 255, 177, 255))

    # Main headline with accent word.
    y = sx(286)
    d.text((sx(64), y), "1 CV ", font=F_HEAD, fill=WHITE)
    cv_width = d.textbbox((sx(64), y), "1 CV ", font=F_HEAD)[2] - sx(64)
    d.text((sx(64) + cv_width, y), "gratis", font=F_HEAD, fill=LIME)
    y += sx(84)
    d.text((sx(64), y), "CV Score", font=F_HEAD_SMALL, fill=WHITE)
    y += sx(84)
    d.text((sx(64), y), "incluido.", font=F_HEAD_SMALL, fill=WHITE)

    body_y = sx(575)
    d.text((sx(64), body_y), "Mejorá tu CV y adaptalo", font=F_BODY, fill=(255, 255, 255, 199))
    d.text((sx(64), body_y + sx(41)), "a una vacante en ", font=F_BODY, fill=(255, 255, 255, 199))
    prefix_w = d.textbbox((sx(64), body_y + sx(41)), "a una vacante en ", font=F_BODY)[2] - sx(64)
    d.text((sx(64) + prefix_w, body_y + sx(41)), "segundos.", font=F_BODY_BOLD, fill=WHITE)
    d.text((sx(64), body_y + sx(82)), "ATS-friendly. Sin inventar experiencia.", font=F_BODY, fill=(255, 255, 255, 199))

    pill_y = sx(708)
    for label, width in [("CV LISTO PARA USAR", 176), ("ATS-FRIENDLY", 132), ("SIN TARJETA", 124)]:
        d.rounded_rectangle((sx(64), pill_y, sx(64 + width), pill_y + sx(42)), radius=sx(10), fill=rgba((255, 255, 255), 0.064), outline=rgba((255, 255, 255), 0.12), width=sx(1))
        d.text((sx(79), pill_y + sx(12)), label, font=F_PILL, fill=(255, 255, 255, 210))
        pill_y += 0
        # advance x by mutating through transform-safe coordinate
        current_left = d.textbbox((0, 0), label, font=F_PILL)[2]
        sx_current = sx(64 + width + 13)
        d._last_x = sx_current  # harmless marker for readability
        sx_left = round(sx_current / SCALE)
        # Update the start x for the next pill by replacing the hardcoded origin.
        if label == "CV LISTO PARA USAR":
            next_x = 64 + width + 13
        elif label == "ATS-FRIENDLY":
            next_x = 64 + 176 + 13 + width + 13
        else:
            next_x = 64
        if label == "CV LISTO PARA USAR":
            # draw second and third explicitly to avoid stateful text layout
            d.rounded_rectangle((sx(next_x), pill_y, sx(next_x + 132), pill_y + sx(42)), radius=sx(10), fill=rgba((255, 255, 255), 0.064), outline=rgba((255, 255, 255), 0.12), width=sx(1))
            d.text((sx(next_x + 15), pill_y + sx(12)), "ATS-FRIENDLY", font=F_PILL, fill=(255, 255, 255, 210))
            third_x = next_x + 132 + 13
            d.rounded_rectangle((sx(third_x), pill_y, sx(third_x + 124), pill_y + sx(42)), radius=sx(10), fill=rgba((255, 255, 255), 0.064), outline=rgba((255, 255, 255), 0.12), width=sx(1))
            d.text((sx(third_x + 15), pill_y + sx(12)), "SIN TARJETA", font=F_PILL, fill=(255, 255, 255, 210))
            break

    device = draw_device()
    overlay.alpha_composite(device, (sx(608), sx(205)))

    # Footer.
    d.text((sx(64), sx(1009)), "worq", font=F_BRAND, fill=WHITE)
    brand_w = d.textbbox((sx(64), sx(1009)), "worq", font=F_BRAND)[2] - sx(64)
    d.text((sx(64) + brand_w, sx(1009)), "ai", font=F_BRAND, fill=LIME)
    d.text((sx(486), sx(1017)), "worqai.io", font=F_KICKER, fill=(255, 255, 255, 122))
    d.rounded_rectangle((sx(872), sx(993), sx(1016), sx(1051)), radius=sx(16), fill=LIME)
    cta = "Probar gratis"
    cta_box = d.textbbox((0, 0), cta, font=F_CTA)
    d.text((sx(944) - (cta_box[2] - cta_box[0]) // 2, sx(1014)), cta, font=F_CTA, fill=(10, 12, 8, 255))

    img.alpha_composite(overlay)

    # Fine grain.
    random.seed(24)
    noise = Image.effect_noise((W, H), 11).convert("L")
    noise_alpha = noise.point(lambda p: int(p * 0.045))
    grain = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    grain.putalpha(noise_alpha)
    img.alpha_composite(grain)

    img.save(OUT_2X)
    img.resize((1080, 1080), Image.Resampling.LANCZOS).save(OUT_1X)
    print(OUT_2X)
    print(OUT_1X)


if __name__ == "__main__":
    main()
