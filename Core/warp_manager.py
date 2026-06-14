import os
import requests
import re
import hashlib
from Core.logger import log

# منابع جدید، معتبر و به‌روز شده مخصوص Warp
WARP_SOURCES = [
    "https://raw.githubusercontent.com/azadi_az_inja_migzare/azadi_az_inja_migzare/main/warp.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/Splitted-By-Protocol/warp.txt",
    "https://raw.githubusercontent.com/sashalsk/V2Ray/main/warp.txt",
    "https://raw.githubusercontent.com/ircfspace/warpsub/main/export/warp"
]

def generate_warp():
    log("🌀 Fetching and validating Warp configs...")
    all_configs = []
    
    for url in WARP_SOURCES:
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                # ۱. استخراج لینک‌های warp://
                warp_uris = re.findall(r'warp://[^\s\n]+', res.text)
                
                # ۲. استخراج لینک‌های wireguard:// (برای سازگاری بیشتر)
                wg_uris = re.findall(r'wireguard://[^\s\n]+', res.text)
                
                # ۳. تمیزسازی: حذف کاراکترهای نامرئی و فاصله‌های اضافی
                raw_matches = warp_uris + wg_uris
                clean_matches = [match.strip() for match in raw_matches if match.strip()]
                
                all_configs.extend(clean_matches)
                log(f"✅ Extracted {len(clean_matches)} potential warp configs from {url}")
        except Exception as e:
            log(f"⚠️ Failed to fetch {url}: {e}")

    # اعتبارسنجی و حذف تکراری‌ها
    unique_configs = []
    seen_hashes = set()
    
    for cfg in all_configs:
        # بررسی ساده اعتبار: باید حداقل شامل warp:// یا wireguard:// و یک @ باشد
        if ('warp://' in cfg or 'wireguard://' in cfg) and '@' in cfg:
            cfg_hash = hashlib.sha256(cfg.encode('utf-8')).hexdigest()
            if cfg_hash not in seen_hashes:
                seen_hashes.add(cfg_hash)
                unique_configs.append(cfg)

    # ذخیره نهایی با تضمین خط جدید
    if unique_configs:
        os.makedirs("output", exist_ok=True)
        with open("output/warp.txt", "w", encoding="utf-8") as f:
            for cfg in unique_configs:
                f.write(cfg + "\n")
        log(f"✅ Generated output/warp.txt with {len(unique_configs)} validated, line-separated configs.")
    else:
        log("⚠️ No valid Warp URIs found in sources. The sources might be temporarily empty or changed format.")
        # اگر فایل قبلی وجود دارد، آن را نگه می‌داریم تا خالی نشود
        if not os.path.exists("output/warp.txt"):
            with open("output/warp.txt", "w", encoding="utf-8") as f:
                f.write("# No valid warp configs found at this time.\n")

if __name__ == "__main__":
    generate_warp()
