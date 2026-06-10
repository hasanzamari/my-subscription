from Core.score import score


def rank(configs):

    data = []

    for c in configs:

        data.append(
            (
                score(c),
                c
            )
        )

    data.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        x[1]
        for x in data
    ]
