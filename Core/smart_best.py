import json, os
from Core.logger import log

def calc_score(info):
    s = info.get("success", 0)
    f = info.get("fail", 0)
    hist = info.get("history", [])
    total = s + f
    
    # ۱. سخت‌گیری مطلق: کانفیگ تست نشده، پایین‌ترین امتیاز ممکن
    if total == 0:
        return -1000.0
        
    # ۲. سخت‌گیری داینامیک: اگر آخرین تست قطع بوده، امتیاز به شدت سرکوب می‌شود
    # (اما -1000 نمی‌شود تا اگر مجبور به پر کردن فایل شدیم، این‌ها آخرین گزینه‌ها باشند)
    if hist and hist[-1] == 9999:
        return 15.0 
        
    # ۳. محاسبه امتیاز پایه بر اساس نرخ موفقیت (حداکثر ۵۰۰)
    base_score = (s / total) * 500
    
    # ۴. قانون سخت‌گیرانه جدید: اگر تعداد شکست‌ها بیشتر از موفقیت‌ها باشد، امتیاز نصف می‌شود!
    if f > s:
        base_score *= 0.5
        
    # ۵. جایزه پینگ (فقط ۵ پینگ موفق اخیر - حداکثر ۲۵۰ امتیاز)
    valid_hist = [x for x in hist if x < 9000]
    if valid_hist:
        recent_pings = valid_hist[-5:]
        avg_recent = sum(recent_pings) / len(recent_pings)
        # اگر پینگ متوسط بالای ۲۵۰ باشد، هیچ امتیازی نمی‌گیرد (سخت‌گیری روی سرعت)
        base_score += max(0, 250 - avg_recent)
        
    # ۶. جایزه پایداری (حداکثر ۱۰۰ امتیاز)
    base_score += min(total, 20) * 5
    
    return round(base_score, 2)

def main():
    log("Loading DB...")
    with open("database/database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    log("Calculating STRICT dynamic scores...")
    for h, info in db.items():
        db[h]["score"] = calc_score(info)
    
    log("Sorting ALL configs by score (descending)...")
    # مرتب‌سازی کل دیتابیس: بالاترین امتیازها مطلقاً در بالای لیست قرار می‌گیرند
    sorted_cfgs = sorted(db.values(), key=lambda x: x.get("score", -1000), reverse=True)
    
    os.makedirs("output", exist_ok=True)
    
    limits = [10, 20, 50, 100, 500, 1000]
    
    for limit in limits:
        path = f"output/Best{limit}.txt"
        
        # تضمین پر شدن فایل: دقیقاً 'limit' تعداد از بالای لیست مرتب‌شده برمی‌داریم
        # چون دیتابیس ۱۶۰ هزار تایی است، همیشه به اندازه کافی کانفیگ برای پر کردن وجود دارد
        selected = sorted_cfgs[:limit]
        
        # نظارت بر کیفیت: کمترین امتیاز در این دسته را ثبت می‌کنیم تا از سخت‌گیری مطمئن شویم
        min_score_in_batch = selected[-1].get("score", -1000) if selected else -1000
        
        with open(path, "w", encoding="utf-8") as f:
            for cfg in selected:
                f.write(cfg.get("config", "") + "\n")
        
        log(f"✅ Wrote {path} ({len(selected)} configs filled. Min score in this batch: {min_score_in_batch})")
    
    log("✅ All Best files generated: STRICT quality, GUARANTEED fullness!")

if __name__ == "__main__":
    main()
