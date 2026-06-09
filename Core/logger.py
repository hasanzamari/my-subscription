import os
from datetime import datetime


LOG_FILE = "logs/log.txt"


def log(message: str):
    os.makedirs("logs", exist_ok=True)

    time = datetime.utcnow().isoformat()
    line = f"[{time}] {message}"

    print(line)

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass
