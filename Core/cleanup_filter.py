def should_delete(info):

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

    if fail >= 20 and success <= 2:
        return True

    if score < 100 and fail >= 10:
        return True

    return False
