from Book.core.entities.base import EntityMarkdownRenderer


class ClassMarkdownRenderer(EntityMarkdownRenderer):
    template_name = "entities/classes/template.md.j2"
