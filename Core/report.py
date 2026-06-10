import json
import os
from datetime import datetime

REPORT = "stats/report.json"


def create_report(stats):

    os.makedirs("stats", exist_ok=True)

    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "stats": stats
    }

    with open(
        REPORT,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False
        )
