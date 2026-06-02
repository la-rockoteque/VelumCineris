from Book.core.entities.base import EntityMarkdownRenderer


class SpellMarkdownRenderer(EntityMarkdownRenderer):
    template_name = "entities/spells/template.md.j2"
