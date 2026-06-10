from Core.logger import log

PROTOCOL_ORDER = [
    "vless://",
    "vmess://",
    "trojan://",
    "hy2://",
    "hysteria://",
    "tuic://",
    "ss://",
    "ssr://",
    "wg://",
    "wireguard://"
]


def sort_configs(configs):

    result = []

    for proto in PROTOCOL_ORDER:

        items = []

        for c in configs:

            if c.startswith(proto):
                items.append(c)

        items.sort()

        result.extend(items)

    log(f"[SORT] total={len(result)}")

    return result
