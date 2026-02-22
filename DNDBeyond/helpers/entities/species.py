from .base import BaseEntity


class SpeciesEntity(BaseEntity):
    entity_type_id = 1743923279
    create_path = "/homebrew/creations/create-species/create"
    edit_path_template = "/homebrew/creations/species/{id}-{slug}/edit"
    list_row_class = "list-row-homebrew-creation-Race"
    list_row_data_type = "races"
    url_segment = "species"

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
                "size": str(data.get("size", "")),
                "speed-walking": data.get("speed_walking", ""),
                "speed-burrowing": data.get("speed_burrowing", ""),
                "speed-climbing": data.get("speed_climbing", ""),
                "speed-flying": data.get("speed_flying", ""),
                "speed-swimming": data.get("speed_swimming", ""),
                "short-description-type": "1",
                "short-description-wysiwyg": data.get("short_description_html", ""),
                "short-description": "",
                "race-group": data.get("race_group", ""),
                "description-type": "1",
                "description-wysiwyg": data.get("description_html", ""),
                "description": "",
                "racial-trait-introduction": data.get("racial_trait_intro", ""),
            }
        )
        return form_data

    def build_update_form_data(self, data):
        return self.build_create_form_data(data)

    def build_files(self, data):
        files = data.get("files")
        if files:
            return files
        return []
