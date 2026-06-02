from Book.core.entities.base import EntityMarkdownRenderer


class DiseaseMarkdownRenderer(EntityMarkdownRenderer):
    template_name = "entities/diseases/template.md.j2"
