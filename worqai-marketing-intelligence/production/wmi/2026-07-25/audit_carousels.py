"""
Audit all carousel HTML files and caption markdown files against strict QA rules:
1. Zero Emojis in text content
2. Zero Dashes (-, –, —) in visible text content
3. Exact CTA: "comenta CV para un mes gratis de WorqAI Pro"
"""
import re
from pathlib import Path

BASE_DIR = Path(r"C:\Users\kenne\OneDrive\Documentos\manifest-claude-system\projects\worqai-marketing-intelligence\production\wmi\2026-07-25")

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+", flags=re.UNICODE
)

DASH_PATTERN = re.compile(r"[-–—]")

EXPECTED_CTA = "comenta CV para un mes gratis de WorqAI Pro"

FILES_TO_CHECK = [
    "carousel_captions.md",
    "carousel_01_dark.html",
    "carousel_02_dark.html",
    "carousel_03_dark.html",
    "carousel_04_light.html",
    "carousel_05_light.html",
    "carousel_06_light.html",
]

def extract_visible_text(html_or_md):
    # Strip style tags
    clean = re.sub(r"<style.*?>.*?</style>", "", html_or_md, flags=re.DOTALL)
    # Strip head tags
    clean = re.sub(r"<head.*?>.*?</head>", "", clean, flags=re.DOTALL)
    # Strip HTML tags
    clean = re.sub(r"<.*?>", " ", clean)
    return clean

def audit():
    report = []
    all_passed = True
    report.append("# QA Audit Results for WorqAI Carousels\n")

    for filename in FILES_TO_CHECK:
        file_path = BASE_DIR / filename
        if not file_path.exists():
            report.append(f"## {filename}: FAIL (File not found)")
            all_passed = False
            continue

        raw_content = file_path.read_text(encoding="utf-8")
        visible_text = extract_visible_text(raw_content)

        emojis_found = EMOJI_PATTERN.findall(visible_text)
        dashes_found = DASH_PATTERN.findall(visible_text)
        has_cta = EXPECTED_CTA in raw_content

        status = True
        notes = []

        if emojis_found:
            status = False
            notes.append(f"Found {len(emojis_found)} emoji(s): {emojis_found}")
        else:
            notes.append("Zero emojis in visible text: PASS")

        if dashes_found:
            status = False
            notes.append(f"Found {len(dashes_found)} dash(es) in visible text: {dashes_found[:5]}")
        else:
            notes.append("Zero dashes in visible text: PASS")

        if has_cta:
            notes.append(f"Exact CTA match ('{EXPECTED_CTA}'): PASS")
        else:
            status = False
            notes.append(f"Exact CTA match ('{EXPECTED_CTA}'): FAIL")

        file_status_str = "PASS" if status else "FAIL"
        if not status:
            all_passed = False

        report.append(f"### `{filename}`: **{file_status_str}**")
        for n in notes:
            report.append(f"- {n}")
        report.append("")

    report_str = "\n".join(report)
    print(report_str)

    qa_report_file = BASE_DIR / "qa_inspection_report.md"
    qa_report_file.write_text(report_str, encoding="utf-8")
    print(f"\nSaved QA report to {qa_report_file}")

if __name__ == "__main__":
    audit()
