import json, os
from Core.logger import log

def calc_hybrid_score(info):
    s = info.get("success", 0)
    f = info.get("fail", 0)
    hist = info.get("history", [])
    total = s + f
    
    # ۱. کانفیگ تست نشده: پایین‌ترین امتیاز ممکن
    if total == 0:
        return -1000.0
        
    # ۲. امتیاز پایه: نرخ موفقیت کلی (حداکثر ۵۰۰)
    # مثال: ۷ موفق از ۱۰ تست = ۷۰٪ * ۵۰۰ = ۳۵۰ امتیاز (سقوط نمی‌کند!)
    base_score = (s / total) * 500
    
    # ۳. بررسی روند اخیر (۵ تست آخر) - عامل لحظه‌ای
    recent_tests = hist[-5:] if len(hist) >= 5 else hist
    if recent_tests:
        recent_successes = sum(1 for x in recent_tests if x < 9000)
        recent_ratio = recent_successes / len(recent_tests)
        
        if recent_ratio >= 0.8:      # ۴ یا ۵ مورد از ۵ مورد اخیر موفق بوده
            base_score += 100        # پاداش عالی
        elif recent_ratio >= 0.6:    # ۳ مورد از ۵ مورد اخیر موفق بوده (مثل مثال شما)
            base_score += 50         # پاداش متوسط
        elif recent_ratio <= 0.2:    # ۰ یا ۱ مورد از ۵ مورد اخیر موفق بوده
            base_score -= 150        # جریمه افت شدید اخیر
        else:
            base_score -= 50         # جریمه خفیف
            
    # ۴. کیفیت پینگ (میانگین پینگ‌های موفق)
    valid_pings = [x for x in hist if x < 9000]
    if valid_pings:
        # برای داینامیک بودن، میانگین ۱۰ پینگ موفق آخر را در نظر می‌گیریم
        recent_valid_pings = valid_pings[-10:]
        avg_ping = sum(recent_valid_pings) / len(recent_valid_pings)
        
        if avg_ping < 150:
            base_score += 150        # پینگ عالی
        elif avg_ping < 300:
            base_score += 100        # پینگ خوب (مثل مثال شما)
        elif avg_ping < 500:
            base_score += 50         # پینگ متوسط
        else:
            base_score += 0          # پینگ بالا، بدون پاداش
            
    # ۵. پاداش پایداری (حداکثر ۵۰ امتیاز برای ۱۰ تست یا بیشتر)
    base_score += min(total, 10) * 5
    
    # امتیاز نهایی هرگز کمتر از صفر نمی‌شود (مگر تست نشده باشد)
    return round(max(0, base_score), 2)

def main():
    log("Loading DB...")
    with open("database/database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    log("Calculating HYBRID dynamic scores (Overall + Recent + Ping)...")
    for h, info in db.items():
        db[h]["score"] = calc_hybrid_score(info)
    
    log("Sorting ALL configs by hybrid score (descending)...")
    # مرتب‌سازی: بالاترین امتیازها در بالا قرار می‌گیرند
    sorted_cfgs = sorted(db.values(), key=lambda x: x.get("score", -1000), reverse=True)
    
    os.makedirs("output", exist_ok=True)
    
    # گسترش لیست‌ها برای پوشش کامل کانفیگ‌های سالم شما
    limits = [10, 20, 50, 100, 500, 1000, 2500, 5000]
    
    for limit in limits:
        path = f"output/Best{limit}.txt"
        seen_configs = set() # ✅ جلوگیری قطعی از تکراری بودن متن کانفیگ
        count = 0
        
        with open(path, "w", encoding="utf-8") as f:
            for cfg in sorted_cfgs:
                config_str = cfg.get("config", "").strip()
                
                # فقط کانفیگ‌های معتبر (امتیاز > 0) و غیرتکراری
                if config_str and config_str not in seen_configs and cfg.get("score", -1000) > 0:
                    seen_configs.add(config_str)
                    f.write(config_str + "\n")
                    count += 1
                    
                # به محض رسیدن به سقف مورد نظر، توقف کن
                if count >= limit:
                    break
        
        # نمایش حداقل امتیاز در این دسته برای نظارت شما
        min_score = sorted_cfgs[count-1].get("score", -1000) if count > 0 else -1000
        log(f"✅ Wrote {path} ({count} UNIQUE configs filled. Min score in batch: {min_score})")
    
    log("✅ Hybrid Best files generated: Balanced, Dynamic, and Fully Populated!")

if __name__ == "__main__":
    main()
