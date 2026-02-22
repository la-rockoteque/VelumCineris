from .base import BaseEntity


class BackgroundEntity(BaseEntity):
    entity_type_id = 1669830167
    create_path = "/homebrew/creations/create-background/create"
    edit_path_template = "/homebrew/creations/backgrounds/{id}-{slug}/edit"
    list_row_class = "list-row-homebrew-creation-Background"
    list_row_data_type = "backgrounds"
    url_segment = "backgrounds"

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
                "short-description-type": "1",
                "short-description-wysiwyg": data.get(
                    "short_description_html", data.get("short_description", "")
                ),
                "short-description": "",
            }
        )
        return form_data

    def build_update_form_data(self, data):
        return self.build_create_form_data(data)
