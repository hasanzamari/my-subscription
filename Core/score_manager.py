from Core.scoring import calculate
from Core.tier import get_tier


def update(info):

    score = calculate(info)

    info["score"] = score

    info["tier"] = get_tier(score)

    return info
