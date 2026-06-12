import json, os
from Core.logger import log

def calc_score(info):
    s = info.get("success", 0)
    f = info.get("fail", 0)
    hist = info.get("history", [])
    total = s + f
    
    # 1. کانفیگ تست نشده
    if total == 0:
        return -1000
        
    # 2. قانون داینامیک واقعی: اگر آخرین تست ناموفق بوده، امتیاز به شدت افت می‌کند
    if hist and hist[-1] == 9999:
        # حتی اگر قبلاً خوب بوده، الان خراب است. امتیاز بسیار پایین می‌گیرد تا از Best خارج شود
        return 15.0 
        
    # 3. محاسبه امتیاز بر اساس نرخ موفقیت
    score = (s / total) * 500
    
    # 4. محاسبه جایزه پینگ (فقط بر اساس ۵ پینگ موفق اخیر برای واکنش سریع‌تر)
    valid_hist = [x for x in hist if x < 9000]
    if valid_hist:
        recent_pings = valid_hist[-5:] # فقط ۵ تای آخر
        avg_recent = sum(recent_pings) / len(recent_pings)
        # پینگ کمتر = امتیاز بیشتر (حداکثر 300 امتیاز)
        score += max(0, 300 - avg_recent)
        
    # 5. جایزه پایداری (حداکثر 100 امتیاز)
    score += min(total, 20) * 5
    
    return round(score, 2)

def main():
    log("Loading DB...")
    with open("database/database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    log("Calculating dynamic scores...")
    for h, info in db.items():
        db[h]["score"] = calc_score(info)
    
    log("Sorting by score (descending)...")
    # مرتب‌سازی: اول امتیاز، اگر مساوی بود کانفیگ جدیدتر (last_seen)
    sorted_cfgs = sorted(db.values(), key=lambda x: (x.get("score", -1000), x.get("last_seen", "")), reverse=True)
    
    # فیلتر فقط کانفیگ‌هایی که امتیاز قابل قبول دارند (بالاتر از 50)
    working_cfgs = [cfg for cfg in sorted_cfgs if cfg.get("score", -1000) > 50]
    
    log(f"Total high-quality working configs found: {len(working_cfgs)}")
    
    os.makedirs("output", exist_ok=True)
    
    # تعریف محدوده‌های یکتا (بدون تکرار)
    ranges = {
        10: (0, 10),
        20: (10, 20),
        50: (20, 50),
        100: (50, 100),
        500: (100, 500),
        1000: (500, 1000)
    }
    
    for limit, (start, end) in ranges.items():
        path = f"output/Best{limit}.txt"
        selected = working_cfgs[start:end]
        
        with open(path, "w", encoding="utf-8") as f:
            for cfg in selected:
                f.write(cfg.get("config", "") + "\n")
        
        log(f"✅ Wrote {path} ({len(selected)} unique configs, rank {start+1}-{end})")
    
    log("✅ All Best files generated with TRUE dynamic scoring!")

if __name__ == "__main__":
    main()
