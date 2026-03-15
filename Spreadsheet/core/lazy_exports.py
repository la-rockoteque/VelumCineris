from __future__ import annotations

from collections.abc import Callable
from typing import Any

Resolver = Callable[[], Any]


def resolve_lazy_attr(
    *,
    module_name: str,
    attr_name: str,
    cache: dict[str, object],
    resolvers: dict[str, Resolver],
    cached_attrs: set[str] | None = None,
):
    """Resolve module attributes lazily with optional per-attribute memoization."""
    resolver = resolvers.get(attr_name)
    if resolver is None:
        raise AttributeError(f"module {module_name!r} has no attribute {attr_name!r}")

    should_cache = cached_attrs is None or attr_name in cached_attrs
    if not should_cache:
        return resolver()

    if attr_name not in cache:
        cache[attr_name] = resolver()
    return cache[attr_name]

