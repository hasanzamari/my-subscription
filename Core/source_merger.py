import os


def load_file(path):

    if not os.path.exists(path):
        return []

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return [
            x.strip()
            for x in f
            if x.strip()
        ]


def merge():

    sources = []

    sources.extend(
        load_file(
            "Sources/Sources.txt"
        )
    )

    sources.extend(
        load_file(
            "Sources/AutoSources.txt"
        )
    )

    return sorted(
        list(
            set(sources)
        )
    )
