#!/usr/bin/env python3
"""
component_picker.py v2 — Smart component picker with compatibility matrices.

Usage:
    py scripts/component_picker.py --system s29 --slides 4 --hook warning --density maximal
    py scripts/component_picker.py --preset brand_worqai_tips
    py scripts/component_picker.py --system s17 --slides 8 --hook negative --density standard

Density modes:
    maximal (default): 4+ techniques per slide, high visual weight
    standard: 3 techniques per slide, balanced weight
"""

import argparse
import json
import random
from pathlib import Path

DATA_PATH = Path(__file__).parent / "component_data.json"


def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_system_info(system_id: str, data: dict):
    systems = data.get("systems", {})
    system = systems.get(system_id, {})
    if not system:
        # Try to find partial match
        for sid, sdata in systems.items():
            if sid.lower() == system_id.lower():
                return sdata, sid
    return system, system_id


def filter_compatible(components: dict, system_id: str, already_selected: list):
    """Filter components compatible with system and not conflicting with selection."""
    result = []
    selected_ids = {c["id"] for c in already_selected}
    selected_conflicts = set()
    for c in already_selected:
        selected_conflicts.update(c.get("conflicts_with", []))

    for comp_id, contract in components.items():
        # Skip already selected
        if comp_id in selected_ids:
            continue
        # Skip if conflicts with already selected
        if comp_id in selected_conflicts:
            continue
        # Check system compatibility
        best_for = contract.get("best_for_systems", "all")
        if best_for != "all" and system_id not in best_for:
            continue
        avoid = contract.get("avoid_systems", [])
        if system_id in avoid:
            continue
        # Check if this component conflicts with already selected
        conflicts = contract.get("conflicts_with", [])
        if any(cid in selected_ids for cid in conflicts):
            continue
        result.append(contract)

    return result


def calculate_slide_weight(selection: list):
    """Sum visual weights of selected components."""
    weight_map = {"low": 1, "medium": 2, "high": 3}
    return sum(weight_map.get(c.get("visual_weight", "medium"), 2) for c in selection)


def suggest_components(system: str = None, slides: int = 8, hook_type: str = None,
                       preset: str = None, brand: str = None, density: str = "maximal",
                       data: dict = None) -> dict:
    if data is None:
        data = load_data()

    # Resolve system
    if preset:
        presets = data.get("layout_maps", {})
        # Presets are actually in carousel-matrix.yaml, not component_data.json
        # For now, use system from preset if available
        system = system or "s17"
    
    system = system or "s17"
    sys_info, resolved_id = get_system_info(system, data)

    # Get layout map
    layout_maps = data.get("layout_maps", {})
    layout_key = f"{slides}_{hook_type}" if hook_type else str(slides)
    slide_layouts = layout_maps.get(layout_key, layout_maps.get("8_negative", {}))

    # Build slide layout assignment
    layouts = {}
    for i in range(1, slides + 1):
        key = f"s{i}"
        layouts[key] = slide_layouts.get(key, "slide-tip-blocks")

    # Density config
    _density_configs = {
        "maximal": {
            "target_techniques_per_slide": 5,
            "max_weight_per_slide": 8,
            "min_weight_per_slide": 5,
            "layer_count": 2,
            "decorative_count": 2,
            "mock_ui_chance": 0.6,
        },
        "standard": {
            "target_techniques_per_slide": 3,
            "max_weight_per_slide": 6,
            "min_weight_per_slide": 3,
            "layer_count": 1,
            "decorative_count": 1,
            "mock_ui_chance": 0.4,
        },
    }
    density_config = _density_configs.get(density, _density_configs["maximal"])

    contracts = data.get("component_contracts", {})

    # Categorize components
    layers = {k: v for k, v in contracts.items() if v.get("category") == "layers"}
    decoratives = {k: v for k, v in contracts.items() if v.get("category") == "decorative"}
    mock_uis = {k: v for k, v in contracts.items() if v.get("category") == "mock-ui"}
    slide_layouts_pool = {k: v for k, v in contracts.items() if v.get("category") == "slides"}

    result = {
        "system": resolved_id,
        "slides": slides,
        "hook_type": hook_type,
        "density": density,
        "slide_plan": {},
        "global_layers": [],
        "notes": [],
    }

    selected_all = []
    global_layers = []

    # Pick 1-2 global layers (background atmosphere shared across slides)
    compatible_layers = filter_compatible(layers, resolved_id, [])
    if compatible_layers:
        # Pick one high-impact layer for global
        global_candidates = [c for c in compatible_layers if c.get("visual_weight") in ("medium", "high")]
        if global_candidates:
            chosen = random.choice(global_candidates)
            global_layers.append(chosen["id"])
            selected_all.append(chosen)

    for slide_num in range(1, slides + 1):
        slide_key = f"s{slide_num}"
        layout_id = layouts.get(slide_key, "slide-tip-blocks")
        slide_selection = []

        # 1. Slide layout
        if layout_id in slide_layouts_pool:
            slide_selection.append(slide_layouts_pool[layout_id])

        # 2. Global layers
        for lid in global_layers:
            if lid in layers:
                slide_selection.append(layers[lid])

        # 3. Per-slide layer (if weight allows)
        current_weight = calculate_slide_weight(slide_selection)
        if current_weight < density_config["max_weight_per_slide"]:
            compatible = filter_compatible(layers, resolved_id, selected_all + slide_selection)
            # Prefer lighter weights for per-slide layers
            compatible.sort(key=lambda c: {"low": 0, "medium": 1, "high": 2}.get(c.get("visual_weight", "medium"), 1))
            for candidate in compatible[:density_config["layer_count"]]:
                if calculate_slide_weight(slide_selection + [candidate]) <= density_config["max_weight_per_slide"]:
                    slide_selection.append(candidate)
                    selected_all.append(candidate)

        # 4. Decoratives
        current_weight = calculate_slide_weight(slide_selection)
        if current_weight < density_config["max_weight_per_slide"]:
            compatible = filter_compatible(decoratives, resolved_id, selected_all + slide_selection)
            # Prioritize decoratives that pair well with already selected
            def pairing_score(c):
                pairs = set(c.get("pairs_well_with", []))
                selected_ids = {s["id"] for s in slide_selection}
                return len(pairs & selected_ids)
            compatible.sort(key=pairing_score, reverse=True)
            for candidate in compatible[:density_config["decorative_count"]]:
                if calculate_slide_weight(slide_selection + [candidate]) <= density_config["max_weight_per_slide"]:
                    slide_selection.append(candidate)
                    selected_all.append(candidate)

        # 5. Mock UI (conditionally)
        current_weight = calculate_slide_weight(slide_selection)
        if current_weight < density_config["max_weight_per_slide"] and random.random() < density_config["mock_ui_chance"]:
            compatible = filter_compatible(mock_uis, resolved_id, selected_all + slide_selection)
            if compatible:
                candidate = random.choice(compatible[:5])
                if calculate_slide_weight(slide_selection + [candidate]) <= density_config["max_weight_per_slide"]:
                    slide_selection.append(candidate)
                    selected_all.append(candidate)

        # Build slide plan
        result["slide_plan"][slide_num] = {
            "layout": layout_id,
            "components": [c["id"] for c in slide_selection],
            "technique_count": sum(c.get("technique_count", 1) for c in slide_selection),
            "visual_weight": calculate_slide_weight(slide_selection),
        }

    result["global_layers"] = global_layers
    result["notes"] = [
        f"Density mode: {density} ({density_config['target_techniques_per_slide']}+ techniques per slide)",
        f"Global layers shared across all slides: {', '.join(global_layers) if global_layers else 'None'}",
        f"Total components selected: {len(selected_all)}",
        f"Visual continuity: maintain same gradient angle and blob rotation across all slides",
    ]

    return result


def format_output(result: dict) -> str:
    lines = []
    lines.append(f"System: {result['system']}")
    lines.append(f"Slides: {result['slides']}")
    lines.append(f"Density: {result['density']}")
    if result.get("hook_type"):
        lines.append(f"Hook: {result['hook_type']}")
    lines.append("")
    lines.append(f"Global layers: {', '.join(result['global_layers']) if result['global_layers'] else 'None'}")
    lines.append("")

    for slide_num, plan in result["slide_plan"].items():
        lines.append(f"Slide {slide_num}: {plan['layout']}")
        lines.append(f"  Components: {', '.join(plan['components'])}")
        lines.append(f"  Techniques: {plan['technique_count']} | Weight: {plan['visual_weight']}")
        lines.append("")

    lines.append("Notes:")
    for note in result["notes"]:
        lines.append(f"  - {note}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Smart carousel component picker v2")
    parser.add_argument("--preset", help="Preset name")
    parser.add_argument("--system", help="System ID (e.g. s29, s17)")
    parser.add_argument("--slides", type=int, default=8, help="Number of slides")
    parser.add_argument("--hook", help="Hook type")
    parser.add_argument("--brand", help="Brand name")
    parser.add_argument("--density", default="maximal", choices=["maximal", "standard"],
                        help="Visual density mode")
    args = parser.parse_args()

    result = suggest_components(
        system=args.system,
        slides=args.slides,
        hook_type=args.hook,
        preset=args.preset,
        brand=args.brand,
        density=args.density,
    )
    print(format_output(result))


if __name__ == "__main__":
    main()
