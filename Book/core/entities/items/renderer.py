from Book.core.entities.base import EntityMarkdownRenderer


class ItemMarkdownRenderer(EntityMarkdownRenderer):
    template_name = "entities/items/template.md.j2"
