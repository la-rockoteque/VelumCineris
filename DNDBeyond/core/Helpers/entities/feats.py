from .base import BaseEntity


class FeatEntity(BaseEntity):
    entity_type_id = 1088085227
    create_path = "/homebrew/creations/create-feat/create"
    edit_path_template = "/homebrew/creations/feats/{id}-{slug}/edit"
    list_row_class = "list-row-homebrew-creation-Feat"
    list_row_data_type = "feats"
    url_segment = "feats"

    def build_create_form_data(self, data):
        form_data = {
            "security-token": self.client.security_token,
            "authenticity-token": self.client.authenticity_token,
        }
        raw = data.get("form_data")
        if raw:
            form_data.update(raw)
            return form_data

        form_data.update(
            {
                "name": data.get("name", ""),
                "version": "",
                "item-description-type": "1",
                "item-description-wysiwyg": data.get(
                    "description_html", data.get("description", "")
                ),
                "item-description": data.get("description", ""),
                "snippet": data.get("snippet", ""),
                "feat-tags-public": data.get("feat_tags", []),
            }
        )
        return form_data

    def build_update_form_data(self, data):
        return self.build_create_form_data(data)
