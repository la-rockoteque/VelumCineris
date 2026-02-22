def normalize_ddb_id(ddb_id):
    """Normalize DDB ID from spreadsheet (handles pandas float conversion)."""
    if ddb_id is None or (hasattr(ddb_id, "__len__") and len(str(ddb_id).strip()) == 0):
        return None

    id_str = str(ddb_id).strip()

    # Strip .0 suffix if present (pandas float conversion)
    if id_str.endswith(".0"):
        id_str = id_str[:-2]

    return id_str if id_str else None


def create_slug(name):
    """Create URL-safe slug from entity name (e.g., 'Fireball' -> 'fireball')."""
    import re

    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug
