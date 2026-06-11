from Core.settings import BEST_CACHE_SIZE
from Core.cache_item import make_item


def update_cache(cache, config, score, tier):

    item = make_item(
        config,
        score,
        tier
    )

    # اگر قبلاً وجود دارد
    for i, old in enumerate(cache):

        if old["config"] == config:

            cache[i] = item
            break

    else:

        cache.append(item)

    cache.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return cache[:BEST_CACHE_SIZE]
