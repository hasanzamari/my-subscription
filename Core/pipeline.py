from Core.parser import parse_sources
from Core.validator import validate_configs
from Core.normalizer import normalize
from Core.smart_filter import filter_configs
from Core.deduplicator import deduplicate_configs


def run_pipeline(raw_sources, db):

    parsed = parse_sources(raw_sources)

    valid = validate_configs(parsed)

    normalized = normalize(valid)

    filtered = filter_configs(normalized)

    unique, removed = deduplicate_configs(
        filtered,
        db
    )

    return {
        "parsed": parsed,
        "valid": valid,
        "normalized": normalized,
        "filtered": filtered,
        "unique": unique,
        "removed": removed
    }
