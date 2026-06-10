import json
import os
from datetime import datetime

FILE = "database/source_health.json"


def load():

    if not os.path.exists(FILE):
        return {}

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save(data):

    os.makedirs("database", exist_ok=True)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def success(url, count, db):

    item = db.get(url, {})

    item["last_run"] = datetime.utcnow().isoformat()
    item["last_configs"] = count
    item["success"] = item.get("success", 0) + 1
    item["failed"] = 0
    item["status"] = "active"

    db[url] = item


def failed(url, db):

    item = db.get(url, {})

    item["last_run"] = datetime.utcnow().isoformat()
    item["failed"] = item.get("failed", 0) + 1
    item["status"] = (
        "disabled"
        if item["failed"] >= 5
        else "active"
    )

    db[url] = item
