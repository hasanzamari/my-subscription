ALLOW = (

    "raw.githubusercontent.com",

    "githubusercontent.com",

    "gist.githubusercontent.com",

    "github.com"

)

KEYWORDS = (

    "sub",

    "subscription",

    "config",

    "configs",

    "v2ray",

    "clash",

    "sing-box",

    "proxy",

    "vpn",

    ".txt",

    ".yaml",

    ".yml",

    ".json"

)


def valid_source(url):

    url = url.lower()

    if not url.startswith(
        ("http://", "https://")
    ):
        return False

    if not any(
        host in url
        for host in ALLOW
    ):
        return False

    if not any(
        key in url
        for key in KEYWORDS
    ):
        return False

    return True
