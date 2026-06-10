import os

PROTOCOLS = {
    "vmess://": "vmess.txt",
    "vless://": "vless.txt",
    "trojan://": "trojan.txt",
    "ss://": "ss.txt",
    "ssr://": "ssr.txt",
    "hy2://": "hy2.txt",
    "hysteria://": "hysteria.txt",
    "tuic://": "tuic.txt",
    "wg://": "wg.txt",
    "wireguard://": "wireguard.txt"
}


def export(configs):

    os.makedirs("output", exist_ok=True)

    files = {}

    for name in PROTOCOLS.values():
        files[name] = []

    for config in configs:

        for proto, filename in PROTOCOLS.items():

            if config.startswith(proto):

                files[filename].append(config)
                break

    for filename, data in files.items():

        with open(
            f"output/{filename}",
            "w",
            encoding="utf-8"
        ) as f:

            f.write("\n".join(data))
