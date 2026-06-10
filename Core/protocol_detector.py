PROTOCOLS = {
    "vmess://": "vmess",
    "vless://": "vless",
    "trojan://": "trojan",
    "ss://": "ss",
    "ssr://": "ssr",
    "hy2://": "hy2",
    "hysteria://": "hysteria",
    "tuic://": "tuic",
    "wg://": "wg",
    "wireguard://": "wireguard"
}


def detect(config):

    if not config:
        return None

    config = config.strip()

    for proto, name in PROTOCOLS.items():

        if config.startswith(proto):
            return name

    return "unknown"
