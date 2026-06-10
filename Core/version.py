import json
import os
from datetime import datetime

FILE = "version.json"


def get_version():

    if not os.path.exists(FILE):

        data = {
            "version": "5.0.0",
            "build": 1,
            "updated": datetime.utcnow().isoformat()
        }

        save_version(data)

        return data

    try:

        with open(FILE, "r", encoding="utf-8") as f:

            return json.load(f)

    except:

        return {
            "version": "5.0.0",
            "build": 1,
            "updated": datetime.utcnow().isoformat()
        }


def save_version(data):

    with open(FILE, "w", encoding="utf-8") as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def increase_build():

    data = get_version()

    data["build"] += 1
    data["updated"] = datetime.utcnow().isoformat()

    save_version(data)

    return data
