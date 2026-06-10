import hashlib
from Core.logger import log


def make_hash(config):
    return hashlib.sha256(
        config.strip().encode("utf-8")
    ).hexdigest()


def deduplicate_configs(configs, db):

    seen = set()
    unique = []
    removed = 0

    for c in configs:

        c = c.strip()

        if not c:
            continue

        h = make_hash(c)

        if h in seen:
            removed += 1
            continue

        seen.add(h)
        unique.append(c)

    log(
        f"[DEDUP] unique={len(unique)} removed={removed}"
    )

    return unique, removed
