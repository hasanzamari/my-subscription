import re
from core.logger import log


def normalize(configs):
    normalized = []

    for c in configs:
        if not c:
            continue

        c = c.strip()

        # حذف فاصله و نویز
        c = re.sub(r"\s+", "", c)

        # یکسان‌سازی پروتکل (case-insensitive)
        c = c.replace("VMESS://", "vmess://")
        c = c.replace("VLESS://", "vless://")
        c = c.replace("TROJAN://", "trojan://")
        c = c.replace("SS://", "ss://")
        c = c.replace("SSR://", "ssr://")

        normalized.append(c)

    log(f"[NORMALIZE] {len(normalized)} configs cleaned")

    return normalized
