import os
import hashlib


def file_hash(path):

    if not os.path.exists(path):
        return None

    h = hashlib.sha256()

    with open(path, "rb") as f:

        while True:

            chunk = f.read(8192)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def check_outputs():

    files = [
        "output/all.txt",
        "database/database.json"
    ]

    result = {}

    for f in files:

        result[f] = file_hash(f)

    return result
