from Core.scoring import calculate


def best(config_db, limit=100):

    result = []

    for config, info in config_db.items():

        score = calculate(info)

        result.append(

            (
                score,
                config
            )

        )

    result.sort(
        reverse=True
    )

    return [

        c

        for _, c in result[:limit]

    ]
