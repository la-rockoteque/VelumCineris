from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from Book.core.markdown.directives import page_break
from Book.core.markdown.helpers import clean_5etools_text, markdown_table, render_entries
import Book.core.markdown.helpers as helpers


@lru_cache(maxsize=1)
def get_environment() -> Environment:
    template_root = Path(__file__).resolve().parents[1]
    env = Environment(
        loader=FileSystemLoader(str(template_root)),
        autoescape=False,
        keep_trailing_newline=True,
        lstrip_blocks=True,
        trim_blocks=True,
        undefined=StrictUndefined,
    )
    env.filters["clean_5etools"] = clean_5etools_text
    env.filters["markdown_table"] = markdown_table
    env.filters["render_entries"] = render_entries
    env.filters["armor_class"] = helpers.armor_class
    env.filters["hit_points"] = helpers.hit_points
    env.filters["item_rarity"] = helpers.item_rarity
    env.filters["join_values"] = helpers.join_values
    env.filters["movement_speed"] = helpers.movement_speed
    env.filters["prerequisite_text"] = helpers.prerequisite_text
    env.filters["spell_components"] = helpers.spell_components
    env.filters["spell_duration"] = helpers.spell_duration
    env.filters["spell_level_school"] = helpers.spell_level_school
    env.filters["spell_range"] = helpers.spell_range
    env.filters["spell_time"] = helpers.spell_time
    env.globals["ability_score_summary"] = helpers.ability_score_summary
    env.globals["attunement_text"] = helpers.attunement_text
    env.globals["higher_level_entries"] = helpers.higher_level_entries
    env.globals["join_mapping"] = helpers.join_mapping
    env.globals["monster_ability_rows"] = helpers.monster_ability_rows
    env.globals["monster_senses"] = helpers.monster_senses
    env.globals["monster_size_type_alignment"] = helpers.monster_size_type_alignment
    env.globals["monster_xp"] = helpers.monster_xp
    env.globals["species_fluff_sections"] = helpers.species_fluff_sections
    env.globals["species_image_url"] = helpers.species_image_url
    env.globals["species_lore_pages"] = helpers.species_lore_pages
    env.globals["species_subtitle"] = helpers.species_subtitle
    env.globals["trait_entries"] = helpers.trait_entries
    env.globals["trait_text_entries"] = helpers.trait_text_entries
    env.globals["page_break"] = page_break
    return env


def render_template(template_name: str, context: dict[str, Any]) -> str:
    return get_environment().get_template(template_name).render(**context)
