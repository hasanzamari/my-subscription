ALLOWED_PROTOCOLS = (
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
)

BEST_LEVELS = [
    10,
    20,
    50,
    100,
    500,
    1000
]


def build_best(db):

    items = []

    for _, info in db.items():

        config = info.get("config")

        if not config:
            continue

        if not config.startswith(ALLOWED_PROTOCOLS):
            continue

        score = info.get(
            "score",
            0
        )

        items.append(
            (
                score,
                config
            )
        )

    items.sort(
        key=lambda x: x[0],
        reverse=True
    )

    result = {}

    for n in BEST_LEVELS:

        result[n] = [
            config
            for _, config in items[:n]
        ]

    return result
