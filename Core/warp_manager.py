import os
import requests
import hashlib
from Core.logger import log

WARP_SOURCES = [
    "https://raw.githubusercontent.com/ircfspace/warpsub/main/export/warp",
    "https://raw.githubusercontent.com/azadi_az_inja_migzare/azadi_az_inja_migzare/main/warp.txt",
    "https://raw.githubusercontent.com/azadi_az_inja_migzare/azadi_az_inja_migzare/main/warp-pro.txt"
]

def generate_warp():
    log("🌀 Fetching Warp configs for emergency use...")
    all_configs = []
    
    for url in WARP_SOURCES:
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                # استخراج هوشمند: خطوطی که حاوی کلمات کلیدی وارپ هستند
                lines = [
                    line.strip() for line in res.text.split('\n') 
                    if line.strip() and any(kw in line.lower() for kw in ['warp://', 'wireguard://', 'wg_port', 'reserved'])
                ]
                all_configs.extend(lines)
                log(f"✅ Fetched {len(lines)} warp configs from {url}")
        except Exception as e:
            log(f"⚠️ Failed to fetch {url}: {e}")

    # حذف تکراری‌ها
    unique_configs = []
    seen_hashes = set()
    for cfg in all_configs:
        cfg_hash = hashlib.sha256(cfg.encode('utf-8')).hexdigest()
        if cfg_hash not in seen_hashes:
            seen_hashes.add(cfg_hash)
            unique_configs.append(cfg)

    if unique_configs:
        os.makedirs("output", exist_ok=True)
        with open("output/warp.txt", "w", encoding="utf-8") as f:
            for cfg in unique_configs:
                f.write(cfg + "\n")
        log(f"✅ Generated output/warp.txt with {len(unique_configs)} unique configs.")
    else:
        log("⚠️ No valid Warp configs found. Keeping old file if exists.")

if __name__ == "__main__":
    generate_warp()
