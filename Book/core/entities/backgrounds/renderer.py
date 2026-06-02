from Book.core.entities.base import EntityMarkdownRenderer


class BackgroundMarkdownRenderer(EntityMarkdownRenderer):
    template_name = "entities/backgrounds/template.md.j2"
