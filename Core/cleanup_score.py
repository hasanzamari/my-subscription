def cleanup_score(info):

    success = info.get(
        "success",
        0
    )

    fail = info.get(
        "fail",
        0
    )

    score = info.get(
        "score",
        0
    )

    total = success + fail

    if total == 0:
        reliability = 0
    else:
        reliability = success / total

    return score + reliability * 200 - fail * 10
