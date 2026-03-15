#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import re
import sys
import textwrap

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from Spreadsheet.sheets import fantasy_sheets


OUTPUT_DIR = Path("assets/art/Species/fantasy")
IMAGE_SIZE = (1024, 1536)
BACKGROUND_COLOR = (235, 235, 235)
TEXT_COLOR = (40, 40, 40)
FONT_PATHS = [
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
NAME_COLUMNS = ["Name", "Species", "Species Name"]


def sanitize_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", name or "").strip("_")
    return cleaned or "Unknown"


def load_font(size: int) -> ImageFont.ImageFont:
    for path in FONT_PATHS:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def get_species_names(df: pd.DataFrame) -> list[str]:
    for column in NAME_COLUMNS:
        if column in df.columns:
            series = df[column].dropna().astype(str).str.strip()
            names = [name for name in series.tolist() if name]
            return sorted(set(names))
    raise ValueError(f"Could not find a species name column in: {list(df.columns)}")


def wrap_text(text: str, width: int = 18) -> str:
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def measure_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> tuple[int, int]:
    bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center", spacing=12)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def fit_font(draw: ImageDraw.ImageDraw, text: str) -> ImageFont.ImageFont:
    max_width = int(IMAGE_SIZE[0] * 0.85)
    max_height = int(IMAGE_SIZE[1] * 0.6)
    for size in range(120, 40, -4):
        font = load_font(size)
        width, height = measure_text(draw, text, font)
        if width <= max_width and height <= max_height:
            return font
    return load_font(40)


def render_placeholder(path: Path, species_name: str, gender_label: str) -> None:
    image = Image.new("RGB", IMAGE_SIZE, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    text = f"{wrap_text(species_name)}\n{gender_label}"
    font = fit_font(draw, text)
    text_width, text_height = measure_text(draw, text, font)
    x = (IMAGE_SIZE[0] - text_width) / 2
    y = (IMAGE_SIZE[1] - text_height) / 2
    draw.multiline_text((x, y), text, font=font, fill=TEXT_COLOR, align="center", spacing=12)
    image.save(path)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df = fantasy_sheets.get_sheet_by_name("species")
    species_names = get_species_names(df)
    for species_name in species_names:
        safe_name = sanitize_name(species_name)
        for suffix, label in [("_M", "Male"), ("_F", "Female")]:
            file_path = OUTPUT_DIR / f"{safe_name}{suffix}.png"
            if file_path.exists():
                continue
            render_placeholder(file_path, species_name, label)


if __name__ == "__main__":
    main()
