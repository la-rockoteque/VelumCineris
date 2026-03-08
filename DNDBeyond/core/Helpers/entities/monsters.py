from .base import BaseEntity


class MonsterEntity(BaseEntity):
    entity_type_id = 779871897
    create_path = "/homebrew/creations/create-monster/create"
    edit_path_template = "/homebrew/creations/monsters/{id}-{slug}/edit"
    list_row_class = "list-row-homebrew-creation-Monster"
    list_row_data_type = "monsters"
    url_segment = "monsters"

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
                "description": data.get("description", ""),
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
