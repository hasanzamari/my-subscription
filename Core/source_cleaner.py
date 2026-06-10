import os


FILE = "Sources/AutoSources.txt"


def clean():

    if not os.path.exists(FILE):
        return

    with open(
        FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = sorted(
            set(
                x.strip()
                for x in f
                if x.strip()
            )
        )

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(data)
        )
