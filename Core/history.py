import json
import os

FILE = "stats/history.json"


def add(stats):

    os.makedirs("stats", exist_ok=True)

    history = []

    if os.path.exists(FILE):

        try:

            with open(
                FILE,
                "r",
                encoding="utf-8"
            ) as f:

                history = json.load(f)

        except:

            history = []

    history.append(stats)

    history = history[-100:]

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            history,
            f,
            indent=2,
            ensure_ascii=False
        )
