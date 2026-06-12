import json
import os
import hashlib
from datetime import datetime, timedelta
from Core.logger import log


EXPIRE_HOURS = 56


def hashlib_sha(text):
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def load_db(path):

    if not os.path.exists(path):
        return {}

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            if isinstance(data, dict):
                return data

    except Exception:
        pass

    return {}


def save_db(path, db):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            db,
            f,
            indent=2,
            ensure_ascii=False
        )


def update_db(db, configs):

    now = datetime.utcnow()
    now_str = now.isoformat()

    new_count = 0
    expired_count = 0

    for config in configs:

        h = hashlib_sha(config)

        if h not in db:

            db[h] = {
                "config": config,
                "first_seen": now_str,
                "last_seen": now_str,
                "score": 0,
                "success": 0,
                "fail": 0
            }

            new_count += 1

        else:

            db[h]["config"] = config
            db[h]["last_seen"] = now_str

            db[h]["score"] = db[h].get(
                "score",
                0
            )

            db[h]["success"] = db[h].get(
                "success",
                0
            )

            db[h]["fail"] = db[h].get(
                "fail",
                0
            )

            if "first_seen" not in db[h]:
                db[h]["first_seen"] = now_str

    remove_list = []

    for h, item in list(db.items()):

        try:

            last = datetime.fromisoformat(
                item["last_seen"]
            )

        except Exception:

            remove_list.append(h)
            continue

        if now - last > timedelta(
            hours=EXPIRE_HOURS
        ):
            remove_list.append(h)

    for h in remove_list:

        del db[h]
        expired_count += 1

    log(
        f"[DB] total={len(db)} "
        f"new={new_count} "
        f"expired={expired_count}"
    )

    return db, new_count, expired_count
