from datetime import datetime


def make_item(
    config,
    score,
    tier
):

    return {

        "config": config,

        "score": score,

        "tier": tier,

        "updated": datetime.utcnow().isoformat()

    }
