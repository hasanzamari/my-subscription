import json, os, base64, urllib.parse
from Core.logger import log

def get_country_boost(info):
    cfg = info.get("config", "").lower()
    search_text = cfg
    if cfg.startswith("vmess://"):
        try:
            b64 = cfg[8:] + "=" * ((4 - len(cfg[8:]) % 4) % 4)
            data = json.loads(base64.b64decode(b64).decode("utf-8", errors="ignore"))
            search_text += " " + str(data.get("ps", "")).lower()
        except: pass
    try:
        search_text += " " + urllib.parse.unquote(cfg).lower()
    except: pass

    tier_1 = ['ae', 'tr', 'fi', 'de', '🇦🇪', '🇹🇷', '🇫🇮', '🇩🇪', 'dubai', 'istanbul', 'frankfurt', 'امارات', 'ترکیه', 'فنلاند', 'آلمان']
    for c in tier_1:
        if c in search_text: return 300

    tier_2 = ['nl', 'fr', 'gb', 'ch', '🇳🇱', '🇫🇷', '🇬🇧', '🇨🇭', 'amsterdam', 'paris', 'london', 'هلند', 'فرانسه', 'انگلیس']
    for c in tier_2:
        if c in search_text: return 200

    tier_3 = ['us', 'ca', 'jp', 'sg', '🇺🇸', '🇨🇦', '🇯🇵', '🇸🇬', 'آمریکا', 'کانادا', 'ژاپن']
    for c in tier_3:
        if c in search_text: return 100

    return 0

def detect_protocol(cfg):
    cfg_lower = cfg.lower()
    if "security=reality" in cfg_lower or "reality" in cfg_lower:
        return "reality"
    if cfg_lower.startswith("vless://"):
        return "vless"
    if cfg_lower.startswith("trojan://"):
        return "trojan"
    if cfg_lower.startswith("vmess://"):
        return "vmess"
    if cfg_lower.startswith("ss://") or cfg_lower.startswith("ssr://"):
        return "shadowsocks"
    return "other"

def calc_final_score(info):
    s, f = info.get("success", 0), info.get("fail", 0)
    total = s + f
    base = 200 if total == 0 else (s / total) * 500
    hist = info.get("history", [])
    if hist and hist[-1] == 9999:
        base *= 0.7
    return round(max(0, base + get_country_boost(info)), 2)

def main():
    log("Loading DB...")
    with open("database/database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    log("Calculating Country-Boosted scores...")
    for h, info in db.items():
        info["final_score"] = calc_final_score(info)
        
    sorted_all = sorted(db.values(), key=lambda x: x.get("final_score", 0), reverse=True)
    
    unique_configs = []
    seen = set()
    for cfg in sorted_all:
        cfg_str = cfg.get("config", "").strip()
        if cfg_str and cfg_str not in seen:
            seen.add(cfg_str)
            unique_configs.append(cfg)
            
    log(f"Total unique configs: {len(unique_configs)}")
    os.makedirs("output", exist_ok=True)
    
    # ۱. ساخت فایل‌های استاندارد (تقسیم‌بندی مجزا)
    limits = [10, 20, 50, 100, 500, 1000, 2500, 5000]
    pos = 0
    for limit in limits:
        path = f"output/Best{limit}.txt"
        selected = unique_configs[pos:pos + limit]
        with open(path, "w", encoding="utf-8") as f:
            for cfg in selected:
                f.write(cfg.get("config", "") + "\n")
        pos += limit

    # ۲. ساخت فایل ویژه best_i.txt
    final_best_i = unique_configs[:100]
    with open("output/best_i.txt", "w", encoding="utf-8") as f:
        for cfg in final_best_i:
            f.write(cfg.get("config", "") + "\n")

    # ۳. ✨ ویژگی پیشرفته: تفکیک بر اساس پروتکل
    protocols = {"vless": [], "vmess": [], "trojan": [], "reality": [], "shadowsocks": []}
    for cfg in unique_configs: # استفاده از کل لیست مرتب شده برای پر کردن فایل‌های پروتکل
        proto = detect_protocol(cfg.get("config", ""))
        if proto in protocols:
            protocols[proto].append(cfg.get("config", ""))
            
    for proto, configs in protocols.items():
        if configs:
            path = f"output/best_{proto}.txt"
            with open(path, "w", encoding="utf-8") as f:
                for c in configs:
                    f.write(c + "\n")
            log(f"✅ Wrote {len(configs)} {proto.upper()} configs to {path}")

    # ۴. ✨ ویژگی پیشرفته: تولید فایل Base64
    all_configs_str = "\n".join([cfg.get("config", "") for cfg in unique_configs])
    base64_encoded = base64.b64encode(all_configs_str.encode('utf-8')).decode('utf-8')
    with open("output/subscription_base64.txt", "w", encoding="utf-8") as f:
        f.write(base64_encoded)
    log("✅ Generated subscription_base64.txt")

    # ۵. ✨ ویژگی پیشرفته: تولید آمار زنده (stats.md)
    country_counts = {}
    for cfg in unique_configs:
        # یک شمارش ساده بر اساس پرچم‌ها و کدهای کشور
        search_text = cfg.get("config", "").lower()
        found = False
        for c in ['🇩🇪', 'de', 'germany', 'آلمان']:
            if c in search_text: country_counts['Germany'] = country_counts.get('Germany', 0) + 1; found = True; break
        if not found:
            for c in ['🇹🇷', 'tr', 'turkey', 'ترکیه']:
                if c in search_text: country_counts['Turkey'] = country_counts.get('Turkey', 0) + 1; found = True; break
        if not found:
            for c in ['🇦🇪', 'ae', 'dubai', 'امارات']:
                if c in search_text: country_counts['UAE'] = country_counts.get('UAE', 0) + 1; found = True; break
        
        if not found:
            country_counts['Other'] = country_counts.get('Other', 0) + 1

    stats_content = f"# 📊 Live Subscription Stats\n\n"
    stats_content += f"- **Total Unique Configs:** `{len(unique_configs)}`\n"
    stats_content += f"- **VLESS:** `{len(protocols['vless'])}`\n"
    stats_content += f"- **VMess:** `{len(protocols['vmess'])}`\n"
    stats_content += f"- **Trojan:** `{len(protocols['trojan'])}`\n"
    stats_content += f"- **Reality:** `{len(protocols['reality'])}`\n\n"
    stats_content += "### 🌍 Top Countries:\n"
    for country, count in sorted(country_counts.items(), key=lambda item: item[1], reverse=True)[:5]:
        stats_content += f"- {country}: `{count}`\n"

    with open("stats.md", "w", encoding="utf-8") as f:
        f.write(stats_content)
    log("✅ Generated stats.md")
    
    log("✅ ALL advanced features generated successfully!")

if __name__ == "__main__":
    main()
