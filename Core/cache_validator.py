def clean(cache):

    seen = set()

    result = []

    for item in cache:

        config = item.get("config")

        if not config:
            continue

        if config in seen:
            continue

        seen.add(config)

        result.append(item)

    return result
