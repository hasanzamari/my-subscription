import os

LOCK_FILE = "runner.lock"


def is_locked():
    return os.path.exists(LOCK_FILE)


def lock():

    with open(
        LOCK_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("running")


def unlock():

    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
