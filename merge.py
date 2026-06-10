from datetime import datetime

from Core.downloader import download_sources
from Core.engine import execute
from Core.database import (
    load_db,
    update_db,
    save_db
)
from Core.exporter import export_all
from Core.final_stats import save as save_final_stats
from Core.logger import log


SOURCES_FILE = "Sources/Sources.txt"
DB_FILE = "database/database.json"


def load_sources():

    with open(
        SOURCES_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return [
            x.strip()
            for x in f
            if x.strip()
        ]


def main():

    log("===== RUN START =====")

    sources = load_sources()

    db = load_db(DB_FILE)

    raw = download_sources(sources)

    result = execute(
        raw,
        db
    )

    final_configs = result["final"]

    db, new_count, expired_count = update_db(
        db,
        final_configs
    )

    save_db(
        DB_FILE,
        db
    )

    export_all(
        final_configs
    )

    save_final_stats(
        len(sources),
        len(result["parsed"]),
        len(result["valid"]),
        len(final_configs)
    )

    log(
        f"[DONE] total={len(final_configs)} "
        f"new={new_count} "
        f"expired={expired_count}"
    )

    log("===== RUN END =====")


if __name__ == "__main__":
    main()
