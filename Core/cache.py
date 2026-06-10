import json
import os

CACHE_FILE = "database/cache.json"


def load_cache():

    if not os.path.exists(CACHE_FILE):
        return {}

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_cache(cache):

    os.makedirs("database", exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            cache,
            f,
            indent=2,
            ensure_ascii=False
        )


def get(url, cache):

    return cache.get(url)


def set(url, value, cache):

    cache[url] = value
