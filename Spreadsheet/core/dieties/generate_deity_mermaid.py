#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
import re
import sys

repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from Spreadsheet.core.Helpers.sheets import fantasy_sheets


def _slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value.strip())
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug.lower() or "deity"


def _build_label(row) -> str:
    name = str(row.get("Name", "")).strip()
    epithet = str(row.get("Epithet", "")).strip()
    parts = [name]
    if epithet:
        parts.append(epithet)
    label = "<Br>".join(_escape_html(p) for p in parts if p)
    return label.replace('"', '\\"')


def _split_links(value: str) -> list[str]:
    if not value:
        return []
    raw = str(value).strip()
    if not raw:
        return []
    parts = re.split(r"[;,]", raw)
    return [part.strip() for part in parts if part.strip()]


def _pantheon_key(value: str) -> str:
    return _slugify(value or "Unassigned")


def _escape_html(value: str) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _split_list(value):
    if pd.isnull(value):
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]


def _load_deity_list() -> list[dict]:
    df_dieties = fantasy_sheets.get_sheet_by_name("deities")
    return [
        {
            "name": row.get("Name"),
            "epithet": row.get("Epithet"),
            "pantheon": row.get("Pantheon"),
            "image": row.get("Image"),
            "domains": _split_list(row.get("Domains")),
            "plane": row.get("Plane"),
            "vstg": row.get("VSTG"),
            "alignment": row.get("Alignment"),
            "followers": row.get("Followers"),
            "symbol": row.get("Symbol"),
            "slogan": row.get("Slogan"),
            "link": row.get("Link"),
            "description": row.get("Description"),
            "lore": row.get("Lore"),
            "quote": row.get("Quote"),
        }
        for _, row in df_dieties.iterrows()
        if pd.notnull(row.get("Name"))
    ]

NESTED_PLANES = {
    "The Veil": {"Orimond"},
    "Orimond": {"The void"},
}

PLANE_STACKS = {
    "Life": [
        "Verdant Cradle",
        "Lithic Bastion",
        "Withered Womb",
    ],
    "Consciousness": [
        "The Murmuring Depths",
        "Murmuring Depth",
        "The Dreamscape",
        "The Throne of Ambitions",
        "The Throne of Ambition",
    ],
}

OUTSIDE_INFINITE_LOOM = {
    "Far Cosmos",
    "The Far Cosmos",
    "Tesserac Leys",
    "Tesseral Leys",
    "The Tesseral Leys",
    "Tesserac",
}


PLANE_GROUP_OVERRIDES = {
    "Pull of light": {
        "The Blinding Ends",
        "The Kindling Plains",
        "Everbright",
    },
    "Pull of Shadow": {
        "The Unraveling Ends",
        "The Unwaking Plains",
        "Nevermourn",
    },
}


def _group_for_plane(plane: str) -> str | None:
    for group_name, planes in PLANE_GROUP_OVERRIDES.items():
        if plane in planes:
            return group_name
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a mermaid graph of deities from a spreadsheet."
    )
    parser.add_argument(
        "--output",
        default="Spreadsheet/dieties/deity_graph.mmd",
        help="Output mermaid file path.",
    )
    args = parser.parse_args()

    diety_list = _load_deity_list()
    dieties = [d for d in diety_list if str(d.get("name", "")).strip()]

    output_path = (repo_root / args.output).resolve() if not Path(args.output).is_absolute() else Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ids_in_use = set()
    lines = ["graph TD"]
    name_to_id = {}
    plane_groups = {}
    ungrouped_planes = {}
    pantheon_colors = {}
    for row in dieties:
        name = str(row.get("name", "")).strip()
        if not name:
            continue
        base_id = f"deity_{_slugify(name)}"
        node_id = base_id
        suffix = 1
        while node_id in ids_in_use:
            suffix += 1
            node_id = f"{base_id}_{suffix}"
        ids_in_use.add(node_id)
        label = _build_label({
            "Name": row.get("name"),
            "Epithet": row.get("epithet"),
        })
        pantheon = str(row.get("pantheon") or "Unassigned").strip() or "Unassigned"
        plane = str(row.get("plane") or "Unassigned").strip() or "Unassigned"
        group = _group_for_plane(plane)
        if group:
            plane_groups.setdefault(group, {})
            plane_groups[group].setdefault(plane, []).append(
                (node_id, label, pantheon)
            )
        else:
            ungrouped_planes.setdefault(plane, []).append(
                (node_id, label, pantheon)
            )
        pantheon_colors.setdefault(pantheon, None)
        name_to_id[name.lower()] = node_id

    pantheon_palette = [
        "#f6c3c0",
        "#c4e3e0",
        "#f3d2a3",
        "#cbd7f2",
        "#d7c3f6",
        "#f0e3b0",
        "#b9e2c8",
        "#f7c7e0",
        "#cde7b0",
        "#d2c1b5",
    ]
    pantheon_class_map = {}
    for index, pantheon in enumerate(sorted(pantheon_colors.keys())):
        class_name = f"pantheon_{_pantheon_key(pantheon)}"
        pantheon_class_map[pantheon] = class_name
        color = pantheon_palette[index % len(pantheon_palette)]
        lines.append(f"classDef {class_name} fill:{color},stroke:#3b3b3b,stroke-width:1px;")

    def render_plane(plane: str, entries, indent: str = "") -> None:
        plane_id = f"plane_{_pantheon_key(plane)}"
        lines.append(f"{indent}subgraph {plane_id}[\"{plane}\"]")
        nested = NESTED_PLANES.get(plane, set())
        for node_id, label, pantheon in entries:
            lines.append(f'{indent}  {node_id}["{label}"]')
            lines.append(f"{indent}  class {node_id} {pantheon_class_map[pantheon]}")
        for child in sorted(nested):
            if child in ungrouped_planes:
                render_plane(child, ungrouped_planes.pop(child), indent + "  ")
        lines.append(f"{indent}end")

    def pop_plane_entries(plane: str):
        for planes in plane_groups.values():
            if plane in planes:
                return planes.pop(plane)
        if plane in ungrouped_planes:
            return ungrouped_planes.pop(plane)
        return None

    def render_plane_stack(stack_label: str, planes: list[str], indent: str = "") -> None:
        stack_entries = []
        seen = set()
        for plane in planes:
            if plane in seen:
                continue
            seen.add(plane)
            entries = pop_plane_entries(plane)
            if entries:
                stack_entries.append((plane, entries))
        if not stack_entries:
            return
        stack_id = f"stack_{_pantheon_key(stack_label)}"
        lines.append(f"{indent}subgraph {stack_id}[\"{stack_label}\"]")
        lines.append(f"{indent}  direction TB")
        for plane, entries in stack_entries:
            render_plane(plane, entries, indent + "  ")
        lines.append(f"{indent}end")

    outside_entries = []
    for plane in sorted(OUTSIDE_INFINITE_LOOM):
        entries = pop_plane_entries(plane)
        if entries:
            outside_entries.append((plane, entries))

    lines.append("subgraph group_infinite_loom[\"The Infinite loom\"]")
    lines.append("  direction LR")

    group_order = ["Pull of light", "Pull of Shadow"]
    group_ids = ["group_infinite_loom"]

    lines.append("  subgraph group_major_rings[\"Major Rings\"]")
    group_ids.append("group_major_rings")
    lines.append("    direction LR")

    lines.append("    subgraph group_core_realms[\"Core Realms\"]")
    group_ids.append("group_core_realms")
    lines.append("      direction LR")

    stack_ids = []
    for stack_label, planes in PLANE_STACKS.items():
        if stack_label not in {"Life", "Consciousness"}:
            continue
        stack_id = f"stack_{_pantheon_key(stack_label)}"
        stack_ids.append(stack_id)
        render_plane_stack(stack_label, planes, indent="      ")

    veil_entries = None
    for plane in list(ungrouped_planes.keys()):
        if plane.lower() == "the veil":
            veil_entries = ungrouped_planes.pop(plane)
            break
    if veil_entries:
        render_plane("The Veil", veil_entries, indent="      ")

    lines.append("    end")

    for group in group_order:
        if group not in plane_groups:
            continue
        group_id = f"group_{_pantheon_key(group)}"
        group_ids.append(group_id)
        lines.append(f"    subgraph {group_id}[\"{group}\"]")
        planes = plane_groups[group]
        for plane in sorted(planes.keys()):
            render_plane(plane, planes[plane], indent="      ")
        lines.append("    end")

    lines.append("  end")

    for stack_label, planes in PLANE_STACKS.items():
        if stack_label in {"Life", "Consciousness"}:
            continue
        stack_id = f"stack_{_pantheon_key(stack_label)}"
        stack_ids.append(stack_id)
        render_plane_stack(stack_label, planes, indent="  ")

    infinite_loom_plane = None
    for plane in list(ungrouped_planes.keys()):
        if plane.lower() == "the infinite loom":
            infinite_loom_plane = ungrouped_planes.pop(plane)
            break
    if infinite_loom_plane:
        for node_id, label, pantheon in infinite_loom_plane:
            lines.append(f'  {node_id}["{label}"]')
            lines.append(f"  class {node_id} {pantheon_class_map[pantheon]}")

    for plane in sorted(list(ungrouped_planes.keys())):
        render_plane(plane, ungrouped_planes[plane], indent="  ")

    lines.append("end")

    group_palette = [
        "#f2e8dc",
        "#e2f0e9",
        "#e8e6f7",
        "#f7e6ef",
        "#f2f0d6",
    ]
    for index, group_id in enumerate(group_ids + stack_ids):
        color = group_palette[index % len(group_palette)]
        lines.append(f"style {group_id} fill:{color},stroke:#555555,color:#000000;")

    for plane, entries in outside_entries:
        render_plane(plane, entries)

    edges = []
    for row in dieties:
        source_name = str(row.get("name", "")).strip()
        if not source_name:
            continue
        source_id = name_to_id.get(source_name.lower())
        if not source_id:
            continue
        for target in _split_links(row.get("link")):
            target_id = name_to_id.get(target.lower())
            if not target_id:
                continue
            edges.append(f"  {source_id} --> {target_id}")

    lines.extend(edges)

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(ids_in_use)} nodes to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
