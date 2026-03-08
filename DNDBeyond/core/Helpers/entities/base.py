class BaseEntity:
    entity_type_id = None
    create_path = None
    edit_path_template = None
    list_row_class = None
    list_row_data_type = None
    url_segment = None
    delete_entity_type_id = None

    def __init__(self, client):
        self.client = client

    def list(self, status: str = "1"):
        try:
            if not self.entity_type_id:
                raise ValueError("entity_type_id is not configured for this entity")
            params = {"filter-type": str(self.entity_type_id)}
            if status is not None:
                params["filter-status"] = str(status)
            response = self.client.get("/my-creations", params=params, timeout=30)
            response.raise_for_status()
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.find_all(
                "div",
                class_=lambda x: x and "list-row-homebrew-creation" in x,
            )
            matched_rows = []
            for row in rows:
                if self.list_row_class:
                    classes = row.get("class", [])
                    if isinstance(classes, str):
                        classes = [classes]
                    if self.list_row_class not in classes:
                        continue
                if self.list_row_data_type:
                    if row.get("data-type") != self.list_row_data_type:
                        continue
                matched_rows.append(row)

            items = []
            for row in matched_rows:
                slug = row.get("data-slug", "")
                if slug:
                    parts = slug.split("-", 1)
                    if parts:
                        item_id = parts[0]
                        item_name = parts[1].replace("-", " ") if len(parts) > 1 else ""
                        items.append({"id": item_id, "name": item_name})
            return items
        except Exception as exc:
            self.client.record_exception(exc)
            return []

    def find_by_name(self, name: str, items=None):
        if items is None:
            items = self.list()
        name_lower = (name or "").lower().strip()
        for item in items:
            item_name = item.get("name", "") or item.get("Name", "") or item.get(
                "title", ""
            )
            if item_name.lower().strip() == name_lower:
                item_id = item.get("id") or item.get("Id") or item.get("itemId")
                return str(item_id) if item_id else None
        return None

    def create(self, data):
        try:
            if not self.create_path:
                raise ValueError("create_path is not configured for this entity")
            form_data = self.build_create_form_data(data)
            files = self.build_files(data)
            response = self.client.post(
                self.create_path,
                data=form_data,
                files=files if files else None,
                allow_redirects=False,
                timeout=30,
            )
            if response.status_code in (302, 303):
                location = response.headers.get("location", "")
                entity_id = self.extract_id_from_location(location)
                if entity_id:
                    return entity_id
                self.client.last_error = f"Could not extract entity ID from: {location}"
                return None
            self.client.record_response_error(
                response, self.client._build_url(self.create_path)
            )
            return None
        except Exception as exc:
            self.client.record_exception(exc)
            return None

    def update(self, entity_id: str, slug: str, data):
        try:
            if not self.edit_path_template:
                raise ValueError("edit_path_template is not configured for this entity")
            path = self.edit_path_template.format(id=entity_id, slug=slug)
            form_data = self.build_update_form_data(data)
            files = self.build_files(data)
            response = self.client.post(
                path,
                data=form_data,
                files=files if files else None,
                allow_redirects=False,
                timeout=30,
            )
            return response.status_code in (302, 303)
        except Exception as exc:
            self.client.record_exception(exc)
            return False

    def delete(self, entity_id: str):
        try:
            entity_type = self.delete_entity_type_id or self.entity_type_id
            if not entity_type:
                raise ValueError("entity_type_id is not configured for this entity")
            path = f"/homebrew/creations/delete?entityTypeId={entity_type}&id={entity_id}"
            form_data = {
                "security-token": self.client.security_token,
                "authenticity-token": self.client.authenticity_token,
                "request-verification-token": self.client.verification_token,
            }
            response = self.client.post(
                path, data=form_data, allow_redirects=False, timeout=30
            )
            if response.status_code == 200:
                return True
            self.client.record_response_error(response, self.client._build_url(path))
            return False
        except Exception as exc:
            self.client.record_exception(exc)
            return False

    def build_create_form_data(self, data):
        raise NotImplementedError

    def build_update_form_data(self, data):
        return self.build_create_form_data(data)

    def build_files(self, data):
        return []

    def extract_id_from_location(self, location: str):
        import re

        if not self.url_segment:
            return None
        match = re.search(rf"/{self.url_segment}/(\d+)-", location)
        if match:
            return match.group(1)
        return None
