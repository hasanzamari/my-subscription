from Core.pipeline import run_pipeline
from Core.ranker import rank
from Core.sorter import sort_configs


def execute(raw_sources, db):

    result = run_pipeline(
        raw_sources,
        db
    )

    ranked = rank(
        result["unique"]
    )

    sorted_configs = sort_configs(
        ranked
    )

    result["final"] = sorted_configs

    return result
