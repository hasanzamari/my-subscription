def calculate_status(info):

    success = info.get("success", 0)

    fail = info.get("fail", 0)

    score = info.get("score", 0)

    if score >= 900:

        return "healthy"

    if score >= 700:

        return "good"

    if score >= 500:

        return "normal"

    if fail >= 10:

        return "weak"

    return "normal"
