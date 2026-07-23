import re
from pathlib import Path

from PIL import Image

ROOT = Path.cwd()

files = sorted(
    ROOT.glob("production/carousel_*_s*.html"),
    key=lambda p: p.stat().st_mtime,
    reverse=True,
)[:10]

for f in files:
    html = f.read_text(encoding="utf-8")
    imgs = re.findall(r'src="\.\./(brand/generated-bg/[^"]+)"', html)
    print(f"\n{f.name}: {len(imgs)} ai-bg images")
    for src in imgs[:4]:
        p = ROOT / src
        with Image.open(p) as im:
            print(f"  {src} {im.size}")
