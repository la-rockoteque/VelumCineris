from Book.core.entities.base import EntityMarkdownRenderer


class LanguageMarkdownRenderer(EntityMarkdownRenderer):
    template_name = "entities/languages/template.md.j2"
