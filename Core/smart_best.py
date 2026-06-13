import json, os, base64
from Core.logger import log

def get_country_boost(info):
    """سیستم امتیازدهی پلکانی بر اساس کیفیت روتینگ به ایران"""
    cfg = info.get("config", "").lower()
    search_text = cfg
    
    # دیکد کردن نام کانفیگ (PS) در صورت vmess بودن
    if cfg.startswith("vmess://"):
        try:
            b64 = cfg[8:] + "=" * ((4 - len(cfg[8:]) % 4) % 4)
            data = json.loads(base64.b64decode(b64).decode("utf-8", errors="ignore"))
            search_text += " " + str(data.get("ps", "")).lower()
        except: pass
    
    # دیکد کردن URL encoding برای خواندن پرچم‌ها
    try:
        import urllib.parse
        search_text += " " + urllib.parse.unquote(cfg).lower()
    except: pass

    # سطح ۱: بهترین روتینگ به ایران (+300 امتیاز)
    tier_1 = ['ae', 'tr', 'fi', 'de', '🇦🇪', '🇹🇷', '🇫🇮', '🇩🇪', 
              'dubai', 'abu dhabi', 'istanbul', 'frankfurt', 'helsinki',
              'امارات', 'ترکیه', 'فنلاند', 'آلمان']
    for c in tier_1:
        if c in search_text: return 300

    # سطح ۲: روتینگ بسیار خوب (+200 امتیاز)
    tier_2 = ['nl', 'fr', 'gb', 'ch', '🇳🇱', '🇫🇷', '🇬🇧', '🇨🇭',
              'amsterdam', 'paris', 'london', 'zurich',
              'هلند', 'فرانسه', 'انگلیس', 'سوئیس']
    for c in tier_2:
        if c in search_text: return 200

    # سطح ۳: روتینگ خوب اما با تاخیر بیشتر (+100 امتیاز)
    tier_3 = ['us', 'ca', 'jp', 'sg', '🇺🇸', '🇨🇦', '🇯🇵', '🇸🇬',
              'new york', 'tokyo', 'singapore',
              'آمریکا', 'کانادا', 'ژاپن', 'سنگاپور']
    for c in tier_3:
        if c in search_text: return 100

    return 0

def calc_final_score(info):
    """امتیاز نهایی فقط بر اساس کشور و پایداری"""
    s, f = info.get("success", 0), info.get("fail", 0)
    total = s + f
    
    # اگر تست نشده، امتیاز متوسط بده (نه صفر)
    if total == 0:
        base = 200
    else:
        # نرخ موفقیت (حداکثر 500)
        base = (s / total) * 500
        
        # اگر آخرین تست قطع بوده، کمی جریمه کن (اما حذف نکن)
        hist = info.get("history", [])
        if hist and hist[-1] == 9999:
            base *= 0.7  # 30% کاهش
    
    # اضافه کردن امتیاز پلکانی کشور
    base += get_country_boost(info)
    
    return round(max(0, base), 2)

def main():
    log("Loading DB...")
    with open("database/database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    log("Calculating scores based on COUNTRY ONLY (no GitHub ping)...")
    for h, info in db.items():
        info["final_score"] = calc_final_score(info)
        
    sorted_all = sorted(db.values(), key=lambda x: x.get("final_score", 0), reverse=True)
    
    # حذف تکراری‌ها
    unique_configs = []
    seen = set()
    for cfg in sorted_all:
        cfg_str = cfg.get("config", "").strip()
        if cfg_str and cfg_str not in seen:
            seen.add(cfg_str)
            unique_configs.append(cfg)
            
    log(f"Total unique configs: {len(unique_configs)}")
    os.makedirs("output", exist_ok=True)
    
    # ساخت فایل‌های استاندارد (تقسیم‌بندی مجزا)
    limits = [10, 20, 50, 100, 500, 1000, 2500, 5000]
    pos = 0
    for limit in limits:
        path = f"output/Best{limit}.txt"
        selected = unique_configs[pos:pos + limit]
        with open(path, "w", encoding="utf-8") as f:
            for cfg in selected:
                f.write(cfg.get("config", "") + "\n")
        pos += limit
        log(f"✅ Wrote {path} ({len(selected)} configs, Rank {pos - limit + 1} to {pos})")

    # ساخت فایل ویژه best_i.txt (100 کانفیگ برتر با بالاترین امتیاز کشور)
    final_best_i = unique_configs[:100]
    with open("output/best_i.txt", "w", encoding="utf-8") as f:
        for cfg in final_best_i:
            f.write(cfg.get("config", "") + "\n")
            
    log(f"👑 Wrote {len(final_best_i)} country-optimized configs to output/best_i.txt")
    log("✅ ALL files generated: Country-Boosted, NO GitHub Ping, ZERO duplicates!")

if __name__ == "__main__":
    main()
