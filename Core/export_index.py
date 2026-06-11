import json
import os


INDEX = "output/index.json"


def build(files):

    with open(
        INDEX,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            files,
            f,
            indent=2,
            ensure_ascii=False
        )
