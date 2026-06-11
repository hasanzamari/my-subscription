from Core.settings import BEST_CACHE_SIZE


def trim(cache):

    if len(cache) <= BEST_CACHE_SIZE:

        return cache

    return cache[:BEST_CACHE_SIZE]
