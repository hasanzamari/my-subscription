import hashlib


def make_hash(config):

    return hashlib.sha256(
        config.encode("utf-8")
    ).hexdigest()


def score(config):

    s = 0

    if config.startswith("vless://"):
        s += 100

    elif config.startswith("vmess://"):
        s += 90

    elif config.startswith("trojan://"):
        s += 80

    elif config.startswith("hy2://"):
        s += 75

    elif config.startswith("hysteria://"):
        s += 70

    elif config.startswith("tuic://"):
        s += 65

    elif config.startswith("ss://"):
        s += 60

    elif config.startswith("ssr://"):
        s += 50

    return s
