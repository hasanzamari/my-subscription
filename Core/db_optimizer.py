def optimize(db):

    optimized = {}

    for h, info in db.items():

        if "config" not in info:
            continue

        optimized[h] = info

    return optimized
