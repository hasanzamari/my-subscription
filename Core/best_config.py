from Core.scoring import calculate


BEST_FILES = [
    10,
    20,
    50,
    100,
    500,
    1000
]


def generate(config_db):

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
        key=lambda x: x[0],
        reverse=True
    )

    outputs = {}

    for limit in BEST_FILES:

        outputs[limit] = [

            c

            for _, c in result[:limit]

        ]

    return outputs
