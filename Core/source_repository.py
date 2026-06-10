import os


AUTO_FILE = "Sources/AutoSources.txt"


def load():

    if not os.path.exists(AUTO_FILE):
        return set()

    with open(
        AUTO_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return set(
            x.strip()
            for x in f
            if x.strip()
        )


def add(url):

    data = load()

    if url in data:
        return False

    data.add(url)

    with open(
        AUTO_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(
                sorted(data)
            )
        )

    return True
