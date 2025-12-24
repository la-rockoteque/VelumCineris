import requests
from typing import Dict, List, Optional

class WorldAnvilAPI:
  """Helper class for World Anvil internal web API interactions"""

  def __init__(self, session: requests.Session, world_id: str, world_slug: str, base_url: str = "https://www.worldanvil.com/api/internal/aboleth"):
    self.session = session
    self.world_id = world_id
    self.world_slug = world_slug
    self.base_url = base_url
    self.last_error = None  # Track last error for debugging

  def get_articles_by_category(self, category_id: str) -> List[Dict]:
    """Get all articles in a specific category using athena/search endpoint

    Based on search.payload.json:
    POST /api/internal/aboleth/athena/search
    Payload: {"categoryId": "...", "limit": 200, "page": 1, ...}

    Handles pagination automatically to get ALL articles in the category.
    """
    try:
      all_articles = []
      page = 1
      limit = 100  # Increased limit to reduce API calls

      while True:
        url = f"{self.base_url}/athena/search"
        payload = {
          "title": "",  # Empty = get all
          "limit": limit,
          "queryFilter": "article",
          "orderBy": "alphabetical",
          "sortDirection": "ASC",
          "categoryId": category_id,
          "page": page
        }

        response = self.session.post(url, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        if not result.get("success"):
          self.last_error = "API returned success=false"
          break

        articles = result.get("articles", [])
        if not articles:
          break

        all_articles.extend(articles)

        # Check if there are more pages
        if len(articles) < limit:
          break

        page += 1

      return all_articles

    except Exception as e:
      self.last_error = str(e)
      print(f"Get articles by category error: {e}")
      return []

  def get_article(self, article_id: str) -> Optional[Dict]:
    """Get full article details by ID"""
    try:
      url = f"{self.base_url}/article"
      params = {
        "granularity": 2,
        "id": article_id
      }
      response = self.session.get(url, params=params, timeout=10)
      response.raise_for_status()
      return response.json()

    except Exception as e:
      self.last_error = str(e)
      print(f"Get article error for '{article_id}': {e}")
      return None

  def create_article(self, data: Dict) -> Optional[Dict]:
    """Create a new article - PUT to /article endpoint (NOT POST!)"""
    try:
      url = f"{self.base_url}/article"

      # Build payload according to real API format from spells.create.payload.json
      payload = {
        "title": data.get("title", ""),
        "world": {"id": self.world_id},  # Object, not string!
        "templateType": data.get("templateType", data.get("template", "article")),
        "state": data.get("state", "private"),
        "content": data.get("content", ""),
        "tags": data.get("tags", "") if isinstance(data.get("tags"), str) else ",".join(data.get("tags", [])),
        "isAdultContent": data.get("isAdultContent", False),
        "allowComments": data.get("allowComments", True),
        "cover": data.get("cover", None),
        "icon": data.get("icon", None),
        "category": None,  # Use "category" not "folderId"
      }

      # Add category if configured
      if "folderId" in data and data["folderId"]:
        payload["category"] = {"id": data["folderId"]}  # Object format
      elif "category" in data and data["category"]:
        payload["category"] = {"id": data["category"]} if isinstance(data["category"], str) else data["category"]

      # Add any template-specific fields
      excluded_keys = {
        "title", "world", "template", "templateType", "state", "content",
        "category", "folderId", "tags", "isAdultContent", "allowComments",
        "cover", "icon"
      }
      for key, value in data.items():
        if key not in excluded_keys and value is not None:
          payload[key] = value

      # CRITICAL: Use PUT, not POST!
      response = self.session.put(url, json=payload, timeout=30)
      response.raise_for_status()
      return response.json()

    except Exception as e:
      self.last_error = str(e)
      print(f"Create error: {e}")
      if hasattr(e, 'response') and e.response is not None:
        print(f"Response status: {e.response.status_code}")
        print(f"Response: {e.response.text[:1000]}")
      return None

  def update_article(self, article_id: str, data: Dict) -> Optional[Dict]:
    """Update an existing article - PATCH to /article?id={id} endpoint"""
    try:
      # CRITICAL: ID goes in query params, not payload!
      url = f"{self.base_url}/article"
      params = {"id": article_id}

      # Build payload - NO ID in payload!
      payload = {
        "title": data.get("title", ""),
        "state": data.get("state", "private"),
        "isDraft": data.get("isDraft", True),
        "isWip": data.get("isWip", True),
        "content": data.get("content", ""),
        "tags": data.get("tags", "") if isinstance(data.get("tags"), str) else ",".join(data.get("tags", [])),
        "icon": data.get("icon", None),
        "cover": data.get("cover", None),
        "isAdultContent": data.get("isAdultContent", False),
        "allowComments": data.get("allowComments", True),
        "subscribergroups": data.get("subscribergroups", []),
        "editor": data.get("editor", "plutarch"),
        "seeded": data.get("seeded", ""),
        "showSeeded": data.get("showSeeded", False),
        "displaySidebar": data.get("displaySidebar", True),
        "displayAuthor": data.get("displayAuthor", False),
        "displayTitle": data.get("displayTitle", True),
        "showInToc": data.get("showInToc", True),
        "displayChildrenUnder": data.get("displayChildrenUnder", True),
        "isEmphasized": data.get("isEmphasized", False),
        "allowContentCopy": data.get("allowContentCopy", False),
        "category": None,
        "articleParent": None,
        "block": None,
      }

      # Handle category
      if "folderId" in data and data["folderId"]:
        payload["category"] = {"id": data["folderId"]}
      elif "category" in data and data["category"]:
        cat = data["category"]
        payload["category"] = {"id": cat} if isinstance(cat, str) else cat

      # Don't include author and world in updates - these are immutable fields set at creation
      # Including them with empty/invalid IDs causes frontend errors

      # Add sidebar content fields
      for field in ["sidepanelcontenttop", "sidepanelcontent", "sidebarcontent",
                    "sidebarcontentbottom", "subheading", "credits", "footnotes",
                    "fullfooter", "authornotes", "pronunciation"]:
        payload[field] = data.get(field, None)

      # Add spell-specific fields if they exist
      spell_fields = [
        "effect", "sideeffects", "manifestation", "source", "discovery",
        "deity", "relatedorganizations", "material", "gestures", "discipline",
        "school", "element", "duration", "castingtime", "spellrange",
        "level", "restrictions"
      ]
      for field in spell_fields:
        if field in data:
          payload[field] = data[field]

      # Add any other template-specific fields
      excluded = {
        "title", "state", "isDraft", "isWip", "content", "tags", "icon",
        "cover", "isAdultContent", "allowComments", "folderId", "category",
        "author_id", "author_name", "world_name", "author", "world",
        "templateType", "template",  # CRITICAL: Cannot update template type!
        "id", "slug", "url", "entityClass", "creationDate", "publicationDate"
      }
      for key, value in data.items():
        if key not in excluded and key not in payload:
          payload[key] = value

      # Use PATCH method with ID in query params
      response = self.session.patch(url, params=params, json=payload, timeout=30)
      response.raise_for_status()
      return response.json()

    except Exception as e:
      self.last_error = str(e)
      print(f"Update error: {e}")
      if hasattr(e, 'response') and e.response is not None:
        print(f"Response status: {e.response.status_code}")
        print(f"Response: {e.response.text[:1000]}")
      return None

  def get_categories(self) -> List[Dict]:
    """Get all article categories"""
    try:
      url = f"{self.base_url}/world/{self.world_id}/categories"
      response = self.session.get(url, timeout=10)
      response.raise_for_status()
      result = response.json()

      # Return categories list
      return result.get("categories", [])

    except Exception as e:
      self.last_error = str(e)
      print(f"Get categories error: {e}")
      return []

  def test_connection(self) -> Dict:
    """Test the connection and return detailed results"""
    try:
      # Try to get world info
      url = f"{self.base_url}/world"
      params = {"id": self.world_id}
      response = self.session.get(url, params=params, timeout=10)
      response.raise_for_status()
      world_data = response.json()

      # Try to get categories
      categories = self.get_categories()

      return {
        "success": True,
        "world": world_data.get("title", "Unknown"),
        "world_id": self.world_id,
        "categories": categories,
        "error": None
      }

    except requests.exceptions.HTTPError as e:
      return {
        "success": False,
        "world": None,
        "world_id": self.world_id,
        "categories": [],
        "error": f"HTTP {e.response.status_code}: {e.response.reason}",
        "details": e.response.text[:500] if hasattr(e, 'response') else str(e)
      }
    except Exception as e:
      return {
        "success": False,
        "world": None,
        "world_id": self.world_id,
        "categories": [],
        "error": str(e),
        "details": None
      }