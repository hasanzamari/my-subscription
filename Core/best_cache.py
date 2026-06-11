import json
import os


CACHE_PATH = "database/best_cache.json"


def load_cache():

    if not os.path.exists(CACHE_PATH):

        return []

    try:

        with open(
            CACHE_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return data.get("top", [])

    except:

        return []


def save_cache(items):

    os.makedirs(
        "database",
        exist_ok=True
    )

    with open(
        CACHE_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "top": items
            },
            f,
            indent=2,
            ensure_ascii=False
        )
