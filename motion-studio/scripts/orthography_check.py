"""
orthography_check.py — scan HTML/JS source for missing Spanish diacritics.

Uses a curated map (high-precision, no guessing) seeded from confirmed regressions
in the Motion Studio codebase. Returns findings with context; never auto-corrects.

Usage:
    py scripts/orthography_check.py templates/scenes/scene-launch-villain-v3.html
    py scripts/orthography_check.py --text "Bilingue y sin Puntuacion"
"""

import re
import sys
import argparse
from pathlib import Path

# ── Curated substitution map ──────────────────────────────────────────────────
# Format: (wrong, correct, word_boundary)
# word_boundary=True: only match whole word (avoids false positives in compounds)
# All patterns are case-insensitive; suggestions preserve original case.

RULES: list[tuple[str, str, bool]] = [
    # Nouns and adjectives — high frequency in this codebase
    ("puntuacion",   "puntuación",   True),
    ("postulacion",  "postulación",  True),
    ("recepcion",    "recepción",    True),
    ("informacion",  "información",  True),
    ("comunicacion", "comunicación", True),
    ("presentacion", "presentación", True),
    ("adaptacion",   "adaptación",   True),
    ("certificacion","certificación",True),
    ("atencion",     "atención",     True),
    ("bilingue",     "bilingüe",     True),
    ("espanol",      "español",      True),
    ("ingles",       "inglés",       True),
    ("frances",      "francés",      True),
    ("generico",     "genérico",     True),
    ("generica",     "genérica",     True),
    ("diagnostico",  "diagnóstico",  True),
    ("grafico",      "gráfico",      True),
    ("debil",        "débil",        True),
    ("exito",        "éxito",        True),
    ("rapido",       "rápido",       True),
    ("practico",     "práctico",     True),
    ("practica",     "práctica",     True),
    ("tecnico",      "técnico",      True),
    ("tecnica",      "técnica",      True),
    ("especifico",   "específico",   True),
    ("especifica",   "específica",   True),
    ("automatico",   "automático",   True),
    ("linea",        "línea",        True),
    ("administracion","administración",True),
    ("logro",        "logro",        False),   # not a diacritic issue — skip
    ("numero",       "número",       True),
    ("numeros",      "números",      True),
    ("pagina",       "página",       True),
    ("minimo",       "mínimo",       True),
    ("maximo",       "máximo",       True),
    ("analisis",     "análisis",     True),
    ("sintesis",     "síntesis",     True),
    ("calculo",      "cálculo",      True),
    ("modulo",       "módulo",       True),
    ("titulo",       "título",       True),
    ("codigo",       "código",       True),
    ("publico",      "público",      True),
    ("publica",      "pública",      True),

    # Adverbs / function words
    ("asi",          "así",          True),
    ("mas",          "más",          True),
    ("tambien",      "también",      True),
    ("ademas",       "además",       True),
    ("solo",         "solo",         False),  # ambiguous (solo/sólo retired in modern RAE)
    ("aqui",         "aquí",         True),
    ("alla",         "allá",         True),
    ("aca",          "acá",          True),

    # First-person preterite verbs (confirmed regressions)
    ("atendi",       "atendí",       True),
    ("resolvi",      "resolví",      True),
    ("trabaje",      "trabajé",      True),
    ("diseñe",       "diseñé",       True),
    ("coordine",     "coordiné",     True),
    ("gestione",     "gestioné",     True),
    ("administre",   "administré",   True),
    ("desarrolle",   "desarrollé",   True),
    ("implemente",   "implementé",   True),
    ("optimice",     "optimicé",     True),
    ("supervise",    "supervisé",    True),
    ("logre",        "logré",        True),
    ("participe",    "participé",    True),
    ("lidere",       "lideré",       True),
    ("mejoré",       "mejoré",       False),  # already correct — skip
    ("estableci",    "establecí",    True),
    ("obtuve",       "obtuve",       False),  # no accent needed
    ("recibi",       "recibí",       True),
    ("produci",      "producí",      True),
    ("construi",     "construí",     True),
    ("mantuve",      "mantuve",      False),  # no accent needed
]

# Filter out no-op rules (same wrong/correct or skip=False)
ACTIVE_RULES = [
    (wrong, correct, wb)
    for wrong, correct, wb in RULES
    if wrong != correct and wrong != "logro"  # logro special-cased to skip
    and not (wrong == "solo" and correct == "solo")
    and not (wrong == "mejoré")
    and not (wrong == "obtuve")
    and not (wrong == "mantuve")
]


def _build_pattern(wrong: str, word_boundary: bool) -> re.Pattern:
    escaped = re.escape(wrong)
    if word_boundary:
        return re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
    return re.compile(escaped, re.IGNORECASE)


_COMPILED: list[tuple[re.Pattern, str]] = [
    (_build_pattern(w, wb), correct)
    for w, correct, wb in ACTIVE_RULES
]


def _preserve_case(original: str, corrected: str) -> str:
    """Match the case pattern of the original word onto the corrected word."""
    if original.isupper():
        return corrected.upper()
    if original[0].isupper():
        return corrected[0].upper() + corrected[1:]
    return corrected


def scan_text(text: str) -> list[tuple[str, str, str]]:
    """
    Scan a plain-text or HTML/JS string for diacritics issues.
    Returns list of (found, suggestion, context_snippet).
    """
    findings = []
    lines = text.splitlines()
    for lineno, line in enumerate(lines, 1):
        for pattern, correct in _COMPILED:
            for m in pattern.finditer(line):
                found = m.group(0)
                suggestion = _preserve_case(found, correct)
                start = max(0, m.start() - 30)
                end   = min(len(line), m.end() + 30)
                ctx   = line[start:end].strip()
                findings.append((found, suggestion, f"line {lineno}: ...{ctx}..."))
    return findings


def scan_html_file(path: Path) -> list[tuple[str, str, str]]:
    """Scan an HTML/JS/JSON file. Returns same format as scan_text."""
    text = path.read_text(encoding="utf-8")
    return scan_text(text)


def main() -> None:
    ap = argparse.ArgumentParser(description="Scan for missing Spanish diacritics")
    ap.add_argument("files", nargs="*", type=Path, help="Files to scan")
    ap.add_argument("--text", type=str, default=None, help="Scan a string directly")
    ap.add_argument("--fail-on-findings", action="store_true",
                    help="Exit 1 if any findings (for preflight integration)")
    args = ap.parse_args()

    all_findings: list[tuple[Path | str, str, str, str]] = []

    if args.text:
        for found, suggestion, ctx in scan_text(args.text):
            all_findings.append(("(inline)", found, suggestion, ctx))

    for path in args.files:
        if not path.exists():
            print(f"WARN: not found: {path}", file=sys.stderr)
            continue
        for found, suggestion, ctx in scan_html_file(path):
            all_findings.append((path, found, suggestion, ctx))

    if not all_findings:
        print("orthography OK — no diacritics issues found")
        sys.exit(0)

    print(f"ORTHOGRAPHY: {len(all_findings)} finding(s)\n")
    for source, found, suggestion, ctx in all_findings:
        print(f"  [{source}]  '{found}' -> '{suggestion}'")
        print(f"    {ctx}")

    if args.fail_on_findings:
        sys.exit(1)


if __name__ == "__main__":
    main()
