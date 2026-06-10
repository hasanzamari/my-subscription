import json
import os
from datetime import datetime

FILE = "stats/final_stats.json"


def save(total, parsed, valid, unique):

    os.makedirs(
        "stats",
        exist_ok=True
    )

    data = {
        "time": datetime.utcnow().isoformat(),
        "total_sources": total,
        "parsed": parsed,
        "valid": valid,
        "unique": unique
    }

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )
