from datetime import datetime


def move(db, graveyard):

    removed = 0

    keep = {}

    for h, info in db.items():

        if info.get("status") != "quarantine":

            keep[h] = info
            continue

        info["graveyard_at"] = datetime.utcnow().isoformat()

        graveyard[h] = info

        removed += 1

    return keep, graveyard, removed
