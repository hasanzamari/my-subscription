from Core.protocol_detector import detect


def filter_configs(configs):

    result = []
    seen = set()

    for config in configs:

        if not config:
            continue

        config = config.strip()

        if len(config) < 10:
            continue

        if detect(config) == "unknown":
            continue

        if config in seen:
            continue

        seen.add(config)
        result.append(config)

    return result
