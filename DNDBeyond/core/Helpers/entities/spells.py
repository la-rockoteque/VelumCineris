from .base import BaseEntity


class SpellEntity(BaseEntity):
    _MODIFIER_TYPE_IDS = {
        "ac": "1",
        "armor class": "1",
        "attack": "2",
        "attack roll": "2",
        "attack rolls": "2",
        "damage": "3",
        "save": "4",
        "saving throw": "4",
        "saving throws": "4",
        "ability check": "5",
        "ability checks": "5",
        "skill": "6",
        "skills": "6",
        "speed": "7",
        "initiative": "8",
        "hp": "9",
        "hit points": "9",
        "temp hp": "10",
        "temporary hit points": "10",
    }
    _MODIFIER_SUBTYPE_IDS = {
        "strength": "1",
        "str": "1",
        "dexterity": "2",
        "dex": "2",
        "constitution": "3",
        "con": "3",
        "intelligence": "4",
        "int": "4",
        "wisdom": "5",
        "wis": "5",
        "charisma": "6",
        "cha": "6",
    }
    _DURATION_UNIT_IDS = {
        "round": "1",
        "rounds": "1",
        "minute": "2",
        "minutes": "2",
        "hour": "3",
        "hours": "3",
        "day": "4",
        "days": "4",
    }
    _TRUE_VALUES = {"1", "true", "y", "yes", "on"}
    entity_type_id = 1118725998
    create_path = "/homebrew/creations/create-spell/create"
    edit_path_template = "/homebrew/creations/spells/{id}-{slug}/edit"
    list_row_class = "list-row-homebrew-creation-Spell"
    list_row_data_type = "spells"
    url_segment = "spells"

    def build_create_form_data(self, data):
        form_data = {
            "security-token": self.client.security_token,
            "authenticity-token": self.client.authenticity_token,
            "Name": data.get("name", ""),
            "version": data.get("version", ""),
            "spell-level": str(data.get("level", 0)),
            "spell-school": str(data.get("school_id", 1)),
            "spell-casting-time": str(data.get("casting_time_id", 1)),
            "spell-activation": str(data.get("activation_id", 1)),
            "spell-casting-time-description": data.get("casting_time_desc", ""),
        }

        if data.get("verbal"):
            form_data["verbal-field"] = "y"
        if data.get("somatic"):
            form_data["somatic-field"] = "y"
        if data.get("material"):
            form_data["material-field"] = "y"
        form_data["spell-components"] = data.get("components_desc", "")

        form_data["origin"] = str(data.get("origin_id", 3))
        range_val = data.get("range", 0)
        form_data["spell-range"] = str(range_val) if range_val > 0 else ""

        form_data["spell-duration"] = str(data.get("duration_id", 1))
        form_data["spell-duration-interval"] = data.get("duration_interval", "")
        form_data["spell-duration-unit"] = data.get("duration_unit", "")

        form_data["spell-description-type"] = "1"
        form_data["spell-description-wysiwyg"] = data.get("description_html", "")
        form_data["spell-description"] = ""

        if data.get("can_cast_at_higher_level"):
            form_data["can-cast-at-higher-level"] = "y"
            form_data["higher-level-scale"] = str(data.get("higher_level_scale", 3))
        else:
            form_data["higher-level-scale"] = ""

        return form_data

    def build_update_form_data(self, data):
        form_data = self.build_create_form_data(data)

        form_data["spell-description"] = data.get("description_html", "")
        form_data["spell-aoe"] = data.get("aoe_type", "")
        form_data["spell-aoe-size"] = data.get("aoe_size", "")
        form_data["attack-type"] = data.get("attack_type", "")
        form_data["spell-save-type"] = data.get("save_type", "")
        form_data["on-miss"] = data.get("on_miss", "")
        form_data["spell-save-success"] = data.get("save_success", "")
        form_data["spell-save-fail"] = data.get("save_fail", "")

        return form_data

    def build_files(self, data):
        classes = data.get("classes", [])
        if isinstance(classes, list):
            return [("class-mapping", (None, str(c))) for c in classes]
        return []

    @staticmethod
    def _normalize_choice_id(value, mapping):
        text = str(value or "").strip()
        if not text:
            return ""
        return mapping.get(text.lower(), text)

    @classmethod
    def _modifier_primary_stat_enabled(cls, modifier_data):
        value = modifier_data.get("primary_stat")
        if value in (None, ""):
            value = modifier_data.get("use_primary_stat")
        return str(value or "").strip().lower() in cls._TRUE_VALUES

    def create_higher_level(self, spell_id, level_data):
        try:
            path = f"/spells/additional/create/{spell_id}"
            form_data = {
                "security-token": self.client.security_token,
                "authenticity-token": self.client.authenticity_token,
                "level": level_data.get("level", ""),
                "modifier": level_data.get("modifier", ""),
                "effect-type": level_data.get("effect_type", "16"),
                "dice-count": level_data.get("dice_count", ""),
                "dice-value": level_data.get("dice_value", ""),
                "dice-fixed": level_data.get("dice_fixed", ""),
                "dice-details": level_data.get("dice_details", ""),
            }
            response = self.client.post(
                path, data=form_data, allow_redirects=False, timeout=30
            )

            if response.status_code == 303:
                return True
            else:
                # Record detailed error for debugging
                self.client.record_response_error(response, self.client._build_url(path))
                return False
        except Exception as exc:
            self.client.record_exception(exc)
            return False

    def create_modifier(self, spell_id, modifier_data):
        try:
            path = f"/spells/modifier/create/{spell_id}"

            modifier_type = self._normalize_choice_id(
                modifier_data.get("modifier_type") or modifier_data.get("type", ""),
                self._MODIFIER_TYPE_IDS,
            )
            modifier_sub_type = self._normalize_choice_id(
                modifier_data.get("modifier_sub_type")
                or modifier_data.get("modifier_subtype")
                or modifier_data.get("sub_type")
                or modifier_data.get("subtype", ""),
                self._MODIFIER_SUBTYPE_IDS,
            )
            dice_count = modifier_data.get("dice_count", "")
            dice_value = modifier_data.get("dice_value") or modifier_data.get("dice_type", "")
            duration = modifier_data.get("duration")
            if duration in (None, ""):
                duration = modifier_data.get("duration_amount", "")
            restriction = modifier_data.get("restriction")
            if restriction in (None, ""):
                restriction = modifier_data.get("details", "")

            form_data = {
                "security-token": self.client.security_token,
                "authenticity-token": self.client.authenticity_token,
                "spell-modifier-type": str(modifier_type),
                "spell-modifier-sub-type": str(modifier_sub_type),
                "dice-count": str(dice_count),
                "dice-value": str(dice_value),
                "fixed-value": str(modifier_data.get("fixed_value", "")),
                "duration": str(duration or ""),
                "duration-unit": str(
                    self._normalize_choice_id(
                        modifier_data.get("duration_unit", ""),
                        self._DURATION_UNIT_IDS,
                    )
                ),
                "restriction": str(restriction or ""),
            }

            if self._modifier_primary_stat_enabled(modifier_data):
                form_data["primary-stat"] = "y"

            response = self.client.post(
                path, data=form_data, allow_redirects=False, timeout=30
            )

            if response.status_code == 303:
                return True
            else:
                # Record detailed error for debugging
                self.client.record_response_error(response, self.client._build_url(path))
                return False
        except Exception as exc:
            self.client.record_exception(exc)
            return False

    def create_condition(self, spell_id, condition_data):
        try:
            path = f"/spells/condition/create/{spell_id}"
            form_data = {
                "security-token": self.client.security_token,
                "authenticity-token": self.client.authenticity_token,
                "condition-effect": condition_data.get("condition_effect", "1"),
                "condition": condition_data.get("condition", ""),
                "condition-duration": condition_data.get("condition_duration", ""),
                "duration-unit": condition_data.get("duration_unit", ""),
                "condition-exception": condition_data.get("condition_exception", ""),
            }
            response = self.client.post(
                path, data=form_data, allow_redirects=False, timeout=30
            )

            if response.status_code == 303:
                return True
            else:
                # Record detailed error for debugging
                self.client.record_response_error(response, self.client._build_url(path))
                return False
        except Exception as exc:
            self.client.record_exception(exc)
            return False

    def get_spell_extras(self, spell_id, slug):
        """Get existing modifiers, conditions, and higher levels from edit page.

        Args:
            spell_id: The spell ID
            slug: The spell slug

        Returns:
            Dict with 'modifiers', 'conditions', 'higher_levels' lists,
            each containing dicts with 'id' and other relevant data
        """
        try:
            from bs4 import BeautifulSoup

            path = f"/homebrew/creations/spells/{spell_id}-{slug}/edit"
            response = self.client.get(path, timeout=30)

            if response.status_code != 200:
                return {'modifiers': [], 'conditions': [], 'higher_levels': []}

            soup = BeautifulSoup(response.text, 'html.parser')
            result = {
                'modifiers': [],
                'conditions': [],
                'higher_levels': []
            }

            # Parse modifiers - look for delete links
            delete_links = soup.find_all('a', href=lambda x: x and '/modifiers/' in x and '/delete' in x)
            for link in delete_links:
                href = link.get('href', '')
                parts = href.split('/')
                if 'modifiers' in parts:
                    idx = parts.index('modifiers')
                    if idx + 1 < len(parts):
                        modifier_id = parts[idx + 1]
                        result['modifiers'].append({'id': modifier_id})

            # Parse conditions
            delete_links = soup.find_all('a', href=lambda x: x and '/conditions/' in x and '/delete' in x)
            for link in delete_links:
                href = link.get('href', '')
                parts = href.split('/')
                if 'conditions' in parts:
                    idx = parts.index('conditions')
                    if idx + 1 < len(parts):
                        condition_id = parts[idx + 1]
                        result['conditions'].append({'id': condition_id})

            # Parse higher levels
            delete_links = soup.find_all('a', href=lambda x: x and '/higher-levels/' in x and '/delete' in x)
            for link in delete_links:
                href = link.get('href', '')
                parts = href.split('/')
                if 'higher-levels' in parts:
                    idx = parts.index('higher-levels')
                    if idx + 1 < len(parts):
                        level_id = parts[idx + 1]
                        result['higher_levels'].append({'id': level_id})

            return result

        except Exception as exc:
            self.client.record_exception(exc)
            return {'modifiers': [], 'conditions': [], 'higher_levels': []}

    def delete_modifier(self, spell_id, modifier_id):
        """Delete a modifier from a spell."""
        try:
            path = f"/spells/modifier/{modifier_id}/delete"
            form_data = {
                "security-token": self.client.security_token,
                "authenticity-token": self.client.authenticity_token,
            }
            response = self.client.post(
                path, data=form_data, allow_redirects=False, timeout=30
            )
            return response.status_code in [200, 303]
        except Exception as exc:
            self.client.record_exception(exc)
            return False

    def delete_condition(self, spell_id, condition_id):
        """Delete a condition from a spell."""
        try:
            path = f"/spells/condition/{condition_id}/delete"
            form_data = {
                "security-token": self.client.security_token,
                "authenticity-token": self.client.authenticity_token,
            }
            response = self.client.post(
                path, data=form_data, allow_redirects=False, timeout=30
            )
            return response.status_code in [200, 303]
        except Exception as exc:
            self.client.record_exception(exc)
            return False

    def delete_higher_level(self, spell_id, level_id):
        """Delete a higher level entry from a spell."""
        try:
            path = f"/spells/additional/{level_id}/delete"
            form_data = {
                "security-token": self.client.security_token,
                "authenticity-token": self.client.authenticity_token,
            }
            response = self.client.post(
                path, data=form_data, allow_redirects=False, timeout=30
            )
            return response.status_code in [200, 303]
        except Exception as exc:
            self.client.record_exception(exc)
            return False

    def get_spell_details(self, spell_id, slug):
        """Get spell details including version and publish status from edit page.

        Args:
            spell_id: The spell ID
            slug: The spell slug

        Returns:
            Dict with 'version' and 'status' (1=published, 2=draft), or empty dict on error
        """
        try:
            from bs4 import BeautifulSoup

            path = f"/homebrew/creations/spells/{spell_id}-{slug}/edit"
            response = self.client.get(path, timeout=30)

            if response.status_code != 200:
                return {}

            soup = BeautifulSoup(response.text, 'html.parser')
            result = {}

            # Extract version from input field
            version_input = soup.find('input', {'id': 'field-version'})
            if version_input:
                result['version'] = version_input.get('value', '').strip()

            # Determine status by checking for publish/unpublish buttons
            # Published spells have an "Unpublish" button
            # Draft spells have a "Submit for Review" or "Publish" button
            unpublish_btn = soup.find('button', text=lambda t: t and 'unpublish' in t.lower())
            submit_btn = soup.find('button', text=lambda t: t and ('submit for review' in t.lower() or 'publish' in t.lower()))

            if unpublish_btn:
                result['status'] = 1  # Published
            elif submit_btn:
                result['status'] = 2  # Draft
            else:
                # Default to draft if we can't determine
                result['status'] = 2

            return result

        except Exception as exc:
            self.client.record_exception(exc)
            return {}

    def publish_spell(self, spell_id):
        """Publish a spell (make it public).

        Args:
            spell_id: The spell ID to publish

        Returns:
            True if successful, False otherwise
        """
        try:
            path = f"/homebrew/creations/spells/{spell_id}/publish"
            form_data = {
                "security-token": self.client.security_token,
                "authenticity-token": self.client.authenticity_token,
            }
            response = self.client.post(
                path, data=form_data, allow_redirects=False, timeout=30
            )
            return response.status_code in [200, 303]
        except Exception as exc:
            self.client.record_exception(exc)
            return False

    def unpublish_spell(self, spell_id):
        """Unpublish a spell (make it private/draft).

        Args:
            spell_id: The spell ID to unpublish

        Returns:
            True if successful, False otherwise
        """
        try:
            path = f"/homebrew/creations/spells/{spell_id}/unpublish"
            form_data = {
                "security-token": self.client.security_token,
                "authenticity-token": self.client.authenticity_token,
            }
            response = self.client.post(
                path, data=form_data, allow_redirects=False, timeout=30
            )
            return response.status_code in [200, 303]
        except Exception as exc:
            self.client.record_exception(exc)
            return False
