from Book.core.entities.base import EntityMarkdownRenderer


class SubclassMarkdownRenderer(EntityMarkdownRenderer):
    template_name = "entities/subclasses/template.md.j2"
