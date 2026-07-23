#!/usr/bin/env python3
"""
contract_injector.py — Auto-generates and injects COMPONENT_CONTRACT headers
into all 181 component HTML files based on their category and visual properties.

Usage:
    py scripts/contract_injector.py --dry-run   # preview changes
    py scripts/contract_injector.py             # apply changes
    py scripts/contract_injector.py --reset     # remove all contract headers
"""

import argparse
import json
import re
from pathlib import Path

COMPONENTS_DIR = Path(".claude/skills/html-carousel-builder/components")
DATA_PATH = Path("scripts/component_data.json")

# Compatibility rules by component category
CATEGORY_RULES = {
    # LAYERS — Geo Grids
    "layers/01-geo-grids": {
        "best_for": ["s02", "s08", "s16", "s19", "s25", "s29", "s33", "s40", "s46"],
        "avoid": ["s03", "s10", "s12", "s18", "s23", "s32", "s36", "s48"],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    # LAYERS — Organic Shapes
    "layers/02-organic-shapes": {
        "best_for": ["s03", "s06", "s10", "s11", "s12", "s18", "s23", "s32", "s36", "s43"],
        "avoid": ["s07", "s19", "s25", "s29", "s46"],
        "visual_weight": "high",
        "technique_count": 1,
    },
    # LAYERS — Light Effects
    "layers/03-light-effects": {
        "best_for": ["s02", "s06", "s08", "s16", "s20", "s21", "s29", "s33", "s37", "s40", "s41"],
        "avoid": ["s05", "s07", "s19", "s23", "s25", "s31", "s39", "s48"],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    # LAYERS — Textures
    "layers/04-textures": {
        "best_for": ["s07", "s18", "s22", "s30", "s32", "s35", "s40", "s42", "s44", "s45"],
        "avoid": ["s05", "s26", "s39"],
        "visual_weight": "low",
        "technique_count": 1,
    },
    # LAYERS — Patterns
    "layers/05-patterns": {
        "best_for": ["s07", "s19", "s24", "s25", "s31", "s34", "s38", "s43", "s45"],
        "avoid": ["s08", "s14", "s33", "s42"],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    # LAYERS — Atmospheric
    "layers/06-atmospheric": {
        "best_for": ["s06", "s21", "s27", "s29", "s30", "s40"],
        "avoid": ["s05", "s19", "s23", "s31", "s39", "s48"],
        "visual_weight": "low",
        "technique_count": 1,
    },
    # LAYERS — Geometric Accents
    "layers/07-geometric-accents": {
        "best_for": ["s01", "s07", "s19", "s25", "s29", "s35", "s37", "s46"],
        "avoid": ["s18", "s23", "s32", "s36"],
        "visual_weight": "low",
        "technique_count": 1,
    },
    # SLIDES — Hooks
    "slides/01-hooks": {
        "best_for": "all",
        "avoid": [],
        "visual_weight": "high",
        "technique_count": 2,
    },
    # SLIDES — Data
    "slides/02-data": {
        "best_for": "all",
        "avoid": [],
        "visual_weight": "high",
        "technique_count": 2,
    },
    # SLIDES — Tips/Errors
    "slides/03-tips-errors": {
        "best_for": "all",
        "avoid": [],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    # SLIDES — Proof
    "slides/04-proof": {
        "best_for": "all",
        "avoid": [],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    # SLIDES — CTA
    "slides/05-cta": {
        "best_for": "all",
        "avoid": [],
        "visual_weight": "high",
        "technique_count": 2,
    },
    # SLIDES — Breaks
    "slides/06-breaks": {
        "best_for": "all",
        "avoid": [],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    # DECORATIVE — Ornaments
    "decorative/01-ornaments": {
        "best_for": ["s01", "s13", "s22", "s23", "s35", "s37", "s42", "s48"],
        "avoid": ["s07", "s19", "s25", "s31"],
        "visual_weight": "low",
        "technique_count": 1,
    },
    # DECORATIVE — Frames
    "decorative/02-frames": {
        "best_for": ["s01", "s07", "s13", "s19", "s22", "s23", "s35", "s42", "s48"],
        "avoid": ["s11", "s24", "s38", "s43"],
        "visual_weight": "low",
        "technique_count": 1,
    },
    # DECORATIVE — Badges
    "decorative/03-badges": {
        "best_for": ["s04", "s07", "s11", "s24", "s31", "s38", "s43"],
        "avoid": ["s01", "s22", "s23", "s42", "s48"],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    # DECORATIVE — Type Accents
    "decorative/04-type-accents": {
        "best_for": ["s01", "s04", "s07", "s13", "s22", "s25", "s35", "s37"],
        "avoid": ["s05", "s26", "s39"],
        "visual_weight": "low",
        "technique_count": 1,
    },
    # DECORATIVE — Chrome
    "decorative/05-chrome": {
        "best_for": ["s08", "s16", "s20", "s29", "s33", "s40"],
        "avoid": ["s18", "s22", "s23", "s30", "s32", "s36"],
        "visual_weight": "low",
        "technique_count": 1,
    },
    # DECORATIVE — Other
    "decorative/deco-press-row": {
        "best_for": ["s07", "s19", "s25"],
        "avoid": ["s03", "s10", "s18", "s23", "s36"],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    "decorative/deco-glass-panel": {
        "best_for": ["s08", "s26", "s33", "s41"],
        "avoid": ["s07", "s22", "s30", "s35"],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    "decorative/deco-stamp": {
        "best_for": ["s01", "s04", "s10", "s13", "s22", "s35"],
        "avoid": ["s08", "s16", "s29", "s33"],
        "visual_weight": "low",
        "technique_count": 1,
    },
    "decorative/deco-progress-bars": {
        "best_for": ["s02", "s08", "s16", "s29", "s33"],
        "avoid": ["s18", "s22", "s30", "s36"],
        "visual_weight": "low",
        "technique_count": 1,
    },
    "decorative/deco-ticker": {
        "best_for": ["s07", "s19", "s25", "s29", "s40"],
        "avoid": ["s03", "s18", "s23", "s36"],
        "visual_weight": "low",
        "technique_count": 1,
    },
    "decorative/deco-watermark": {
        "best_for": ["s01", "s13", "s22", "s23", "s35", "s42"],
        "avoid": ["s05", "s11", "s24", "s38"],
        "visual_weight": "low",
        "technique_count": 1,
    },
    # MOCK-UI — Terminals
    "mock-ui/01-terminals": {
        "best_for": ["s02", "s08", "s16", "s29", "s33", "s40", "s46"],
        "avoid": ["s03", "s10", "s12", "s18", "s22", "s23", "s30", "s36", "s48"],
        "visual_weight": "high",
        "technique_count": 2,
    },
    # MOCK-UI — CV Mocks
    "mock-ui/02-cv-mocks": {
        "best_for": ["s02", "s05", "s08", "s12", "s17", "s23", "s33", "s48"],
        "avoid": ["s06", "s21", "s27", "s29", "s40"],
        "visual_weight": "high",
        "technique_count": 2,
    },
    # MOCK-UI — App Frames
    "mock-ui/03-app-frames": {
        "best_for": ["s02", "s05", "s08", "s16", "s26", "s33", "s41"],
        "avoid": ["s07", "s22", "s30", "s35"],
        "visual_weight": "high",
        "technique_count": 2,
    },
    # MOCK-UI — Code Blocks
    "mock-ui/04-code-blocks": {
        "best_for": ["s02", "s08", "s16", "s29", "s33", "s40", "s46"],
        "avoid": ["s03", "s10", "s18", "s23", "s36", "s48"],
        "visual_weight": "medium",
        "technique_count": 2,
    },
    # MOCK-UI — Forms
    "mock-ui/05-forms": {
        "best_for": ["s02", "s05", "s08", "s17", "s26", "s31", "s33", "s39", "s48"],
        "avoid": ["s06", "s21", "s27", "s29", "s40"],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    # MOCK-UI — Data Displays
    "mock-ui/06-data-displays": {
        "best_for": ["s02", "s08", "s14", "s16", "s29", "s33", "s40", "s46"],
        "avoid": ["s18", "s22", "s23", "s30", "s36"],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    # MOCK-UI — Messaging
    "mock-ui/06-messaging": {
        "best_for": ["s02", "s05", "s08", "s16", "s26", "s33", "s41"],
        "avoid": ["s07", "s22", "s30", "s35"],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    # MOCK-UI — E-commerce
    "mock-ui/07-ecommerce": {
        "best_for": ["s01", "s04", "s10", "s13", "s24", "s38", "s43"],
        "avoid": ["s07", "s19", "s25", "s29", "s46"],
        "visual_weight": "medium",
        "technique_count": 1,
    },
    # MOCK-UI — Icons
    "mock-ui/08-icons": {
        "best_for": "all",
        "avoid": [],
        "visual_weight": "low",
        "technique_count": 1,
    },
}

# Pairing suggestions by category
PAIRING_RULES = {
    "layers/01-geo-grids": ["light-neon-border", "deco-progress-dots", "mock-terminal-mac", "deco-masthead"],
    "layers/02-organic-shapes": ["light-glow-radial-center", "deco-ornament", "deco-watermark"],
    "layers/03-light-effects": ["geo-circuit-board", "mock-terminal-mac", "deco-brand-anchor"],
    "layers/04-textures": ["deco-stamp", "deco-corner-frame", "slide-pull-quote"],
    "layers/05-patterns": ["deco-badge-tag", "slide-big-number", "mock-metric-card"],
    "layers/06-atmospheric": ["deco-ticker", "slide-cinematic-title", "mock-app-browser"],
    "layers/07-geometric-accents": ["deco-corner-frame", "deco-border-double", "slide-editorial-index"],
    "mock-ui/01-terminals": ["geo-circuit-board", "light-neon-border", "atm-scan-lines", "deco-progress-dots"],
    "mock-ui/02-cv-mocks": ["org-blob-corner", "light-glow-accent", "deco-watermark"],
    "mock-ui/03-app-frames": ["geo-wireframe-flat", "light-glow-radial-corner", "deco-brand-anchor"],
    "mock-ui/04-code-blocks": ["geo-circuit-board", "light-volumetric-beam", "deco-masthead"],
    "mock-ui/05-forms": ["pat-stripe-diagonal", "deco-badge-ribbon", "deco-counter-circle"],
    "mock-ui/06-data-displays": ["geo-dot-grid", "deco-progress-bars", "mock-display-badge-row"],
    "mock-ui/06-messaging": ["org-blob-scattered", "light-glow-accent", "deco-swipe-pill"],
    "mock-ui/07-ecommerce": ["pat-checkerboard", "deco-badge-tag", "ecom-pricing-table"],
    "mock-ui/08-icons": ["deco-brand-anchor", "deco-progress-dots", "icon-social"],
}

CONFLICT_RULES = {
    "layers/01-geo-grids": ["org-blob-scattered", "tex-paper-fibers", "pat-waves-subtle"],
    "layers/02-organic-shapes": ["geo-circuit-board", "geo-hex-grid", "geo-wireframe-perspective"],
    "layers/03-light-effects": ["tex-grain-heavy", "tex-scratch-overlay"],
    "layers/04-textures": ["light-lens-flare", "light-ambient-orb"],
    "layers/05-patterns": ["org-marble-vein", "tex-noise-color"],
    "layers/06-atmospheric": ["light-volumetric-beam", "light-neon-border"],
    "layers/07-geometric-accents": ["org-ink-splash", "org-smoke-trail"],
    "mock-ui/01-terminals": ["mock-cv-lines", "mock-app-iphone", "frame-polaroid"],
    "mock-ui/02-cv-mocks": ["mock-terminal-mac", "mock-code-syntax-light"],
    "mock-ui/03-app-frames": ["mock-terminal-minimal", "mock-cv-two-column"],
    "mock-ui/04-code-blocks": ["mock-form-input", "mock-checklist"],
    "mock-ui/05-forms": ["mock-terminal-windows", "mock-code-diff"],
    "mock-ui/06-data-displays": ["mock-app-chat", "message-chat"],
    "mock-ui/06-messaging": ["mock-metric-card", "mock-display-table-mini"],
    "mock-ui/07-ecommerce": ["mock-terminal-mac", "mock-code-syntax-light"],
    "mock-ui/08-icons": ["deco-masthead", "deco-ticker"],
}


def get_category_rules(rel_path: str):
    """Find the best matching rules for a component path."""
    # Try exact match first
    if rel_path in CATEGORY_RULES:
        return CATEGORY_RULES[rel_path]
    # Try parent directory match
    parent = str(Path(rel_path).parent).replace("\\", "/")
    if parent in CATEGORY_RULES:
        return CATEGORY_RULES[parent]
    # Try grandparent
    grandparent = str(Path(rel_path).parent.parent).replace("\\", "/")
    if grandparent in CATEGORY_RULES:
        return CATEGORY_RULES[grandparent]
    # Default
    return {"best_for": "all", "avoid": [], "visual_weight": "medium", "technique_count": 1}


def get_pairings(rel_path: str):
    parent = str(Path(rel_path).parent).replace("\\", "/")
    grandparent = str(Path(rel_path).parent.parent).replace("\\", "/")
    return PAIRING_RULES.get(rel_path, PAIRING_RULES.get(parent, PAIRING_RULES.get(grandparent, [])))


def get_conflicts(rel_path: str):
    parent = str(Path(rel_path).parent).replace("\\", "/")
    grandparent = str(Path(rel_path).parent.parent).replace("\\", "/")
    return CONFLICT_RULES.get(rel_path, CONFLICT_RULES.get(parent, CONFLICT_RULES.get(grandparent, [])))


def estimate_file_size(filepath: Path):
    """Estimate visual impact based on file content."""
    content = filepath.read_text(encoding="utf-8")
    kb = len(content) / 1024
    if kb < 0.5:
        return 1.0
    elif kb < 1.5:
        return 2.5
    elif kb < 3.0:
        return 4.0
    else:
        return 6.0


def build_contract(filepath: Path, rel_path: str) -> dict:
    """Build the contract dict for a component."""
    comp_id = filepath.stem
    category = str(Path(rel_path).parts[0])
    rules = get_category_rules(rel_path)
    pairings = get_pairings(rel_path)
    conflicts = get_conflicts(rel_path)
    size_impact = estimate_file_size(filepath)

    contract = {
        "id": comp_id,
        "category": category,
        "technique_count": rules.get("technique_count", 1),
        "visual_weight": rules.get("visual_weight", "medium"),
        "file_size_impact_kb": round(size_impact, 1),
    }

    best_for = rules.get("best_for", "all")
    if best_for != "all":
        contract["best_for_systems"] = best_for
    avoid = rules.get("avoid", [])
    if avoid:
        contract["avoid_systems"] = avoid
    if pairings:
        contract["pairs_well_with"] = pairings
    if conflicts:
        contract["conflicts_with"] = conflicts

    return contract


def format_contract(contract: dict) -> str:
    """Format contract as HTML comment."""
    lines = ["<!--", "COMPONENT_CONTRACT:"]
    json_str = json.dumps(contract, indent=2, ensure_ascii=False)
    for line in json_str.splitlines():
        lines.append(f"  {line}")
    lines.append("-->")
    return "\n".join(lines)


def remove_existing_contract(content: str) -> str:
    """Remove existing COMPONENT_CONTRACT comment."""
    pattern = re.compile(r"<!--\s*COMPONENT_CONTRACT:.*?-->", re.DOTALL)
    return pattern.sub("", content).strip()


def process_all(dry_run: bool = False):
    if not COMPONENTS_DIR.exists():
        print(f"ERROR: Components directory not found: {COMPONENTS_DIR}")
        return

    total = 0
    modified = 0
    for filepath in COMPONENTS_DIR.rglob("*.html"):
        # Skip the shell base
        if filepath.name == "shell-base.html":
            continue
        rel_path = str(filepath.relative_to(COMPONENTS_DIR)).replace("\\", "/")
        contract = build_contract(filepath, rel_path)
        contract_block = format_contract(contract)

        content = filepath.read_text(encoding="utf-8")
        cleaned = remove_existing_contract(content)
        new_content = f"{contract_block}\n\n{cleaned}"

        total += 1
        if dry_run:
            print(f"[DRY-RUN] {rel_path}")
            print(f"  id: {contract['id']}")
            print(f"  weight: {contract['visual_weight']}")
            print(f"  best_for: {contract.get('best_for_systems', 'all')}")
            print()
        else:
            filepath.write_text(new_content, encoding="utf-8")
            modified += 1
            if modified % 20 == 0:
                print(f"  ... {modified} components injected")

    if not dry_run:
        print(f"\nDONE: {modified} components updated with contracts.")
    else:
        print(f"\nDRY-RUN: {total} components would be updated.")


def reset_all():
    """Remove all contract headers."""
    total = 0
    for filepath in COMPONENTS_DIR.rglob("*.html"):
        content = filepath.read_text(encoding="utf-8")
        cleaned = remove_existing_contract(content)
        if cleaned != content.strip():
            filepath.write_text(cleaned, encoding="utf-8")
            total += 1
    print(f"RESET: Removed contracts from {total} components.")


def main():
    parser = argparse.ArgumentParser(description="Inject component contract headers")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--reset", action="store_true", help="Remove all contracts")
    args = parser.parse_args()

    if args.reset:
        reset_all()
    else:
        process_all(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
