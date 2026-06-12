import json, os
from Core.logger import log

def calc_score(info):
    s, f = info.get("success", 0), info.get("fail", 0)
    hist = info.get("history", [])
    total = s + f
    if total == 0:
        return -1000
    score = (s / total) * 500
    valid_hist = [x for x in hist if x < 9000]
    if valid_hist:
        median = sorted(valid_hist)[len(valid_hist)//2]
        score += max(0, 300 - median)
    score += min(total, 20) * 10
    return round(score, 2)

def main():
    log("Loading DB...")
    with open("database/database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    log("Calculating scores...")
    for h, info in db.items():
        db[h]["score"] = calc_score(info)
    
    log("Sorting...")
    sorted_cfgs = sorted(db.values(), key=lambda x: (x.get("score", -1000), x.get("last_seen", "")), reverse=True)
    
    # فیلتر فقط کانفیگ‌های با امتیاز مثبت
    working_cfgs = [cfg for cfg in sorted_cfgs if cfg.get("score", -1000) > 0]
    
    log(f"Total working configs: {len(working_cfgs)}")
    
    os.makedirs("output", exist_ok=True)
    
    # تعریف محدوده‌ها به صورت یکتا (بدون تکرار)
    ranges = {
        10: (0, 10),      # رتبه ۱-۱۰
        20: (10, 20),     # رتبه ۱۱-۲۰
        50: (20, 50),     # رتبه ۲۱-۵۰
        100: (50, 100),   # رتبه ۵۱-۱۰۰
        500: (100, 500),  # رتبه ۱۰۱-۵۰۰
        1000: (500, 1000) # رتبه ۵۰۱-۱۰۰۰
    }
    
    for limit, (start, end) in ranges.items():
        path = f"output/Best{limit}.txt"
        selected = working_cfgs[start:end]
        
        with open(path, "w", encoding="utf-8") as f:
            for cfg in selected:
                f.write(cfg.get("config", "") + "\n")
        
        log(f"✅ Wrote {path} ({len(selected)} unique configs, rank {start+1}-{end})")
    
    log("✅ All Best files generated with NO duplicates!")

if __name__ == "__main__":
    main()
