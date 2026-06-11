from Core.cache_validator import clean
from Core.cache_sort import sort_cache


def merge(old_cache, new_items):

    cache = old_cache.copy()

    cache.extend(new_items)

    cache = clean(cache)

    cache = sort_cache(cache)

    return cache
