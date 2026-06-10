import os
from Core.logger import log

OUTPUT_DIR = "output"

FILES = {
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


def export_all(configs):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # فایل اصلی
    with open(
        os.path.join(OUTPUT_DIR, "all.txt"),
        "w",
        encoding="utf-8"
    ) as f:

        for c in configs:
            f.write(c.strip() + "\n")

    # فایل‌های جداگانه
    for proto, filename in FILES.items():

        with open(
            os.path.join(OUTPUT_DIR, filename),
            "w",
            encoding="utf-8"
        ) as f:

            for c in configs:

                if c.startswith(proto):
                    f.write(c.strip() + "\n")

    log(
        f"[EXPORT] total={len(configs)}"
    )
