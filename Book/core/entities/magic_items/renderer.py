from Book.core.entities.base import EntityMarkdownRenderer


class MagicItemMarkdownRenderer(EntityMarkdownRenderer):
    template_name = "entities/magic_items/template.md.j2"
