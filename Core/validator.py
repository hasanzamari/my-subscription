from Core.logger import log

VALID_PROTOCOLS = (
    "vmess://",
    "vless://",
    "trojan://",
    "ss://",
    "ssr://",
    "hy2://",
    "hysteria://",
    "tuic://",
    "wg://",
    "wireguard://",
    "socks://",
    "http://",
    "https://"
)

def validate_configs(configs):

    valid = []
    seen = set()

    for config in configs:

        if not config:
            continue

        config = config.strip()

        if len(config) < 5:
            continue

        if "<html" in config.lower():
            continue

        if not config.startswith(VALID_PROTOCOLS):
            continue

        if config not in seen:
            seen.add(config)
            valid.append(config)

    log(f"[VALIDATE] valid={len(valid)}")

    return valid
