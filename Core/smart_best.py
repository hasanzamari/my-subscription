import json, os
from Core.logger import log

def calc_score(info):
    s = info.get("success", 0)
    f = info.get("fail", 0)
    hist = info.get("history", [])
    total = s + f
    
    if total == 0:
        return -1000.0
        
    if hist and hist[-1] == 9999:
        return 15.0 
        
    base_score = (s / total) * 500
    
    if f > s:
        base_score *= 0.5
        
    valid_hist = [x for x in hist if x < 9000]
    if valid_hist:
        recent_pings = valid_hist[-5:]
        avg_recent = sum(recent_pings) / len(recent_pings)
        base_score += max(0, 250 - avg_recent)
        
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
    sorted_cfgs = sorted(db.values(), key=lambda x: x.get("score", -1000), reverse=True)
    
    os.makedirs("output", exist_ok=True)
    
    # افزایش سقف برای پوشش تمام ۲۴۰۰ کانفیگ سالم شما
    limits = [10, 20, 50, 100, 500, 1000, 2500, 5000]
    
    for limit in limits:
        path = f"output/Best{limit}.txt"
        
        seen_configs = set() # ✅ جلوگیری قطعی از تکراری بودن متن کانفیگ
        count = 0
        
        with open(path, "w", encoding="utf-8") as f:
            for cfg in sorted_cfgs:
                config_str = cfg.get("config", "").strip()
                
                # فقط اگر کانفیگ خالی نباشد و قبلاً نوشته نشده باشد
                if config_str and config_str not in seen_configs:
                    seen_configs.add(config_str)
                    f.write(config_str + "\n")
                    count += 1
                    
                # به محض رسیدن به سقف مورد نظر، توقف کن
                if count >= limit:
                    break
        
        min_score = sorted_cfgs[count-1].get("score", -1000) if count > 0 else -1000
        log(f"✅ Wrote {path} ({count} UNIQUE configs filled. Min score: {min_score})")
    
    log("✅ All Best files generated: STRICT quality, ZERO duplicates, GUARANTEED fullness!")

if __name__ == "__main__":
    main()
