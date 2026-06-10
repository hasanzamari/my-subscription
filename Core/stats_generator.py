import json
import os
from datetime import datetime

FILE = "stats/protocol_stats.json"

PROTOCOLS = [
    "vmess://",
    "vless://",
    "trojan://",
    "ss://",
    "ssr://",
    "hy2://",
    "hysteria://",
    "tuic://",
    "wg://",
    "wireguard://"
]


def generate(configs):

    data = {
        "generated_at": datetime.utcnow().isoformat(),
        "total": len(configs)
    }

    for p in PROTOCOLS:

        count = 0

        for c in configs:

            if c.startswith(p):
                count += 1

        data[p.replace("://", "")] = count

    os.makedirs("stats", exist_ok=True)

    with open(
        FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )

    return data
