from Core.source_ranker import load


def get_best(limit=None):

    db = load()

    items = sorted(
        db.items(),
        key=lambda x: x[1].get("score", 0),
        reverse=True
    )

    urls = [x[0] for x in items]

    if limit:
        return urls[:limit]

    return urls
