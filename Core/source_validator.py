KEYWORDS = [

    "raw",

    "raw.githubusercontent",

    "githubusercontent",

    "github.com",

    "blob",

    "refs/heads",

    "raw/main",

    "main",

    "master",

    "sub",

    "subs",

    "subscription",

    "subscriptions",

    "subscribe",

    "config",

    "configs",

    "proxy",

    "proxies",

    "vpn",

    "v2ray",

    "xray",

    "clash",

    "mihomo",

    "sing-box",

    "singbox",

    "base64",

    "node",

    "nodes",

    "share",

    "links",

    "url",

    "urls",

    "list",

    "mix",

    "full",

    "all",

    "free",

    "public",

    "wireguard",

    "wg",

    "trojan",

    "vmess",

    "vless",

    "hy2",

    "hysteria",

    "tuic",

    ".txt",

    ".yaml",

    ".yml",

    ".json"

]


def valid_source(url):

    if not url:
        return False

    url = url.strip().lower()

    if not (
        url.startswith("http://")
        or
        url.startswith("https://")
    ):
        return False

    return any(
        k in url
        for k in KEYWORDS
    )
