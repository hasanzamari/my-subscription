from datetime import datetime


def build(files, stats):

    return {

        "time": datetime.utcnow().isoformat(),

        "files": files,

        "stats": stats

    }
