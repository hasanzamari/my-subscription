from datetime import datetime


def move_to_quarantine(info):

    info["status"] = "quarantine"

    info["quarantine_since"] = datetime.utcnow().isoformat()

    return info
