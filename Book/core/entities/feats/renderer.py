from Book.core.entities.base import EntityMarkdownRenderer


class FeatMarkdownRenderer(EntityMarkdownRenderer):
    template_name = "entities/feats/template.md.j2"
