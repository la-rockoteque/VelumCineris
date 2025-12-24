class DnDBeyondAPI:
  """Helper class for D&D Beyond homebrew API"""

  def __init__(self, session, security_token: str, authenticity_token: str, verification_token: str = None):
    self.session = session
    self.security_token = security_token
    self.authenticity_token = authenticity_token
    self.verification_token = verification_token
    self.base_url = "https://www.dndbeyond.com"
    self.last_error = None
    self.last_response = None

  @staticmethod
  def normalize_ddb_id(ddb_id):
    """Normalize DDB ID from spreadsheet (handles pandas float conversion)

    Pandas reads numeric columns as float64, so 3135829 becomes 3135829.0
    This function strips the .0 suffix to get the proper ID string.
    """
    if ddb_id is None or (hasattr(ddb_id, '__len__') and len(str(ddb_id).strip()) == 0):
      return None

    id_str = str(ddb_id).strip()

    # Strip .0 suffix if present (pandas float conversion)
    if id_str.endswith('.0'):
      id_str = id_str[:-2]

    return id_str if id_str else None

  @staticmethod
  def create_slug(spell_name):
    """Create URL-safe slug from spell name (e.g., 'Fireball' -> 'fireball')"""
    import re
    # Convert to lowercase, replace spaces and special chars with hyphens
    slug = spell_name.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug

  def get_user_spells(self):
    try:
      url = f"{self.base_url}/my-creations"
      params = {"filter-type": "1118725998", "filter-status": "1"}
      response = self.session.get(url, params=params, timeout=30)
      response.raise_for_status()
      from bs4 import BeautifulSoup
      soup = BeautifulSoup(response.text, 'html.parser')
      spells = []
      spell_rows = soup.find_all('div', {'class': lambda x: x and 'list-row-homebrew-creation-Spell' in x})
      for row in spell_rows:
        slug = row.get('data-slug', '')
        if slug:
          parts = slug.split('-', 1)
          if parts:
            spell_id = parts[0]
            # Don't use .title() - keep original slug format to match source data
            # "blink-and-you-missed-it" -> "blink and you missed it"
            spell_name = parts[1].replace('-', ' ') if len(parts) > 1 else ''
            spells.append({"id": spell_id, "name": spell_name})
      return spells
    except Exception as e:
      self.last_error = str(e)
      return []

  def find_spell_by_name(self, name: str, user_spells=None):
    if user_spells is None:
      user_spells = self.get_user_spells()
    name_lower = name.lower().strip()
    for spell in user_spells:
      spell_name = spell.get("name", "") or spell.get("Name", "") or spell.get("title", "")
      if spell_name.lower().strip() == name_lower:
        spell_id = spell.get("id") or spell.get("Id") or spell.get("spellId")
        return str(spell_id) if spell_id else None
    return None

  def create_spell(self, data):
    try:
      url = f"{self.base_url}/homebrew/creations/create-spell/create"

      form_data = {
        "security-token": self.security_token,
        "authenticity-token": self.authenticity_token,
        "Name": data.get("name", ""),
        "version": "",
        "spell-level": str(data.get("level", 0)),
        "spell-school": str(data.get("school_id", 1)),
        "spell-casting-time": str(data.get("casting_time_id", 1)),
        "spell-activation": str(data.get("activation_id", 1)),
        "spell-casting-time-description": data.get("casting_time_desc", ""),
      }

      # Components
      if data.get("verbal"):
        form_data["verbal-field"] = "y"
      if data.get("somatic"):
        form_data["somatic-field"] = "y"
      if data.get("material"):
        form_data["material-field"] = "y"
      form_data["spell-components"] = data.get("components_desc", "")

      # Range/Origin - CRITICAL: Send empty string when range is 0
      form_data["origin"] = str(data.get("origin_id", 3))
      range_val = data.get("range", 0)
      form_data["spell-range"] = str(range_val) if range_val > 0 else ""

      # Duration
      form_data["spell-duration"] = str(data.get("duration_id", 1))
      form_data["spell-duration-interval"] = data.get("duration_interval", "")
      form_data["spell-duration-unit"] = data.get("duration_unit", "")

      # Description
      form_data["spell-description-type"] = "1"
      form_data["spell-description-wysiwyg"] = data.get("description_html", "")
      form_data["spell-description"] = ""

      # Higher level - CRITICAL: Always send, even if empty
      if data.get("can_cast_at_higher_level"):
        form_data["can-cast-at-higher-level"] = "y"
        form_data["higher-level-scale"] = str(data.get("higher_level_scale", 3))
      else:
        form_data["higher-level-scale"] = ""

      # Classes
      classes = data.get("classes", [])
      files = [("class-mapping", (None, str(c))) for c in classes] if isinstance(classes, list) else []

      response = self.session.post(url, data=form_data, files=files if files else None, allow_redirects=False, timeout=30)
      self.last_response = response

      if response.status_code == 303:
        location = response.headers.get("location", "")
        import re
        match = re.search(r'/spells/(\d+)-', location)
        if match:
          return match.group(1)
        self.last_error = f"Could not extract spell ID from: {location}"
        return None
      else:
        error_details = {
          "status_code": response.status_code,
          "reason": response.reason,
          "url": url,
          "headers": dict(response.headers),
        }
        try:
          if response.headers.get('content-type', '').startswith('application/json'):
            error_details["response_body"] = response.json()
          else:
            error_details["response_preview"] = response.text[:500]
        except:
          pass
        self.last_error = error_details
        print(f"\n⚠️  Detailed error information:")
        print(f"   Status: {error_details['status_code']} {error_details['reason']}")
        return None
    except Exception as e:
      import traceback
      error_details = {
        "exception_type": type(e).__name__,
        "exception_message": str(e),
        "traceback": traceback.format_exc()
      }
      self.last_error = error_details
      print(f"\n⚠️  Exception: {error_details['exception_type']}: {error_details['exception_message']}")
      return None

  def update_basic_information(self, spell_id, slug, data):
    """Update basic information for an existing spell (includes AOE, attack, save fields)"""
    try:
      url = f"{self.base_url}/homebrew/creations/spells/{spell_id}-{slug}/edit"

      form_data = {
        "security-token": self.security_token,
        "authenticity-token": self.authenticity_token,
        "Name": data.get("name", ""),
        "version": "",
        "spell-level": str(data.get("level", 0)),
        "spell-school": str(data.get("school_id", 1)),
        "spell-casting-time": str(data.get("casting_time_id", 1)),
        "spell-activation": str(data.get("activation_id", 1)),
        "spell-casting-time-description": data.get("casting_time_desc", ""),
      }

      # Components
      if data.get("verbal"):
        form_data["verbal-field"] = "y"
      if data.get("somatic"):
        form_data["somatic-field"] = "y"
      if data.get("material"):
        form_data["material-field"] = "y"
      form_data["spell-components"] = data.get("components_desc", "")

      # Range/Origin
      form_data["origin"] = str(data.get("origin_id", 3))
      range_val = data.get("range", 0)
      form_data["spell-range"] = str(range_val) if range_val > 0 else ""

      # Duration
      form_data["spell-duration"] = str(data.get("duration_id", 1))
      form_data["spell-duration-interval"] = data.get("duration_interval", "")
      form_data["spell-duration-unit"] = data.get("duration_unit", "")

      # Description
      form_data["spell-description-type"] = "1"
      form_data["spell-description-wysiwyg"] = data.get("description_html", "")
      form_data["spell-description"] = data.get("description_html", "")

      # Higher level
      if data.get("can_cast_at_higher_level"):
        form_data["can-cast-at-higher-level"] = "y"
        form_data["higher-level-scale"] = str(data.get("higher_level_scale", 3))
      else:
        form_data["higher-level-scale"] = ""

      # Additional fields not in create
      form_data["spell-aoe"] = data.get("aoe_type", "")
      form_data["spell-aoe-size"] = data.get("aoe_size", "")
      form_data["attack-type"] = data.get("attack_type", "")
      form_data["spell-save-type"] = data.get("save_type", "")
      form_data["on-miss"] = data.get("on_miss", "")
      form_data["spell-save-success"] = data.get("save_success", "")
      form_data["spell-save-fail"] = data.get("save_fail", "")

      # Classes
      classes = data.get("classes", [])
      files = [("class-mapping", (None, str(c))) for c in classes] if isinstance(classes, list) else []

      response = self.session.post(url, data=form_data, files=files if files else None, allow_redirects=False, timeout=30)
      self.last_response = response

      return response.status_code == 303
    except Exception as e:
      import traceback
      self.last_error = {
        "exception_type": type(e).__name__,
        "exception_message": str(e),
        "traceback": traceback.format_exc()
      }
      return False

  def create_higher_level(self, spell_id, level_data):
    """Add higher level scaling to a spell"""
    try:
      url = f"{self.base_url}/homebrew/creations/spells/{spell_id}/higher-levels/create"

      form_data = {
        "security-token": self.security_token,
        "authenticity-token": self.authenticity_token,
        "level": level_data.get("level", ""),
        "modifier": level_data.get("modifier", ""),
        "effect-type": level_data.get("effect_type", "16"),  # 16 = damage
        "dice-count": level_data.get("dice_count", ""),
        "dice-value": level_data.get("dice_value", ""),
        "dice-fixed": level_data.get("dice_fixed", ""),
        "dice-details": level_data.get("dice_details", ""),
      }

      response = self.session.post(url, data=form_data, allow_redirects=False, timeout=30)
      self.last_response = response

      return response.status_code == 303
    except Exception as e:
      import traceback
      self.last_error = {
        "exception_type": type(e).__name__,
        "exception_message": str(e),
        "traceback": traceback.format_exc()
      }
      return False

  def create_modifier(self, spell_id, modifier_data):
    """Add a modifier to a spell (stat bonuses, effects, etc.)"""
    try:
      url = f"{self.base_url}/homebrew/creations/spells/{spell_id}/modifiers/create"

      form_data = {
        "security-token": self.security_token,
        "authenticity-token": self.authenticity_token,
        "spell-modifier-type": modifier_data.get("modifier_type", ""),
        "spell-modifier-sub-type": modifier_data.get("modifier_sub_type", ""),
        "dice-count": modifier_data.get("dice_count", ""),
        "dice-value": modifier_data.get("dice_value", ""),
        "fixed-value": modifier_data.get("fixed_value", ""),
        "duration": modifier_data.get("duration", ""),
        "duration-unit": modifier_data.get("duration_unit", ""),
        "restriction": modifier_data.get("restriction", ""),
      }

      response = self.session.post(url, data=form_data, allow_redirects=False, timeout=30)
      self.last_response = response

      return response.status_code == 303
    except Exception as e:
      import traceback
      self.last_error = {
        "exception_type": type(e).__name__,
        "exception_message": str(e),
        "traceback": traceback.format_exc()
      }
      return False

  def create_condition(self, spell_id, condition_data):
    """Add a condition to a spell (blinded, poisoned, etc.)"""
    try:
      url = f"{self.base_url}/homebrew/creations/spells/{spell_id}/conditions/create"

      form_data = {
        "security-token": self.security_token,
        "authenticity-token": self.authenticity_token,
        "condition-effect": condition_data.get("condition_effect", "1"),  # 1 = grants condition
        "condition": condition_data.get("condition", ""),
        "condition-duration": condition_data.get("condition_duration", ""),
        "duration-unit": condition_data.get("duration_unit", ""),
        "condition-exception": condition_data.get("condition_exception", ""),
      }

      response = self.session.post(url, data=form_data, allow_redirects=False, timeout=30)
      self.last_response = response

      return response.status_code == 303
    except Exception as e:
      import traceback
      self.last_error = {
        "exception_type": type(e).__name__,
        "exception_message": str(e),
        "traceback": traceback.format_exc()
      }
      return False

  def delete_spell(self, spell_id, spell_name):
    """Delete a spell from D&D Beyond

    Args:
        spell_id: The D&D Beyond spell ID
        spell_name: The spell name (used to create slug)

    Returns:
        bool: True if deletion succeeded, False otherwise
    """
    try:
      url = f"{self.base_url}/homebrew/creations/delete?entityTypeId=1118725998&id={spell_id}"

      form_data = {
        "security-token": self.security_token,
        "authenticity-token": self.authenticity_token,
        "request-verification-token": self.verification_token
      }

      response = self.session.post(url, data=form_data, allow_redirects=False, timeout=30)
      self.last_response = response

      # Successful deletion returns 200 redirect to /my-creations
      if response.status_code == 200:
        return True
      else:
        self.last_error = {
          "status_code": response.status_code,
          "reason": response.reason,
          "url": url
        }
        return False
    except Exception as e:
      import traceback
      self.last_error = {
        "exception_type": type(e).__name__,
        "exception_message": str(e),
        "traceback": traceback.format_exc()
      }
      return False