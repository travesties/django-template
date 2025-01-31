from contextlib import contextmanager

from django.core.cache import cache


@contextmanager
def managed_cache_value(key: str, default):
    """
    Context manager that maintains a lock around the requested
    cache resource while utilized by the caller.

    Usage:
        with managed_cache_value(key="cache-key") as resource:
            ...do stuff...
    """
    lock_cache_key = f"Lock_{key}"

    while not cache.add(lock_cache_key, True, 180):
        pass

    try:
        cache_value = cache.get(key, default)
        yield cache_value
    finally:
        cache.delete(lock_cache_key)