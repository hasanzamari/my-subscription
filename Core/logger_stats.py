from datetime import datetime
import json
import os

FILE = "stats/run_history.json"


def save_run(data):

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

    history.append({

        "time": datetime.utcnow().isoformat(),

        "sources": data.get("sources"),

        "parsed": data.get("parsed"),

        "valid": data.get("valid"),

        "unique": data.get("unique")

    })

    history = history[-200:]

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
