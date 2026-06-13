import json, os, base64, requests, time, socket
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from Core.logger import log

PREFERRED_COUNTRIES = ['de', 'tr', 'ae', 'nl', 'fi', 'fr', 'gb', 'ch', '🇩🇪', '🇹🇷', '🇦🇪', '🇳🇱', '🇫🇮', '🇫🇷', '🇬🇧', '🇨🇭', 'germany', 'turkey', 'uae', 'dubai']

def extract_addr_port(cfg):
    try:
        cfg = cfg.strip()
        if cfg.startswith("vmess://"):
            b64 = cfg[8:] + "=" * ((4 - len(cfg[8:]) % 4) % 4)
            data = json.loads(base64.b64decode(b64).decode("utf-8", errors="ignore"))
            return str(data.get("add") or data.get("address")), str(data.get("port"))
        if "://" in cfg:
            p = urlparse(cfg)
            addr, port = p.hostname, p.port
            if not addr and "@" in p.netloc:
                parts = p.netloc.split("@")[-1].split(":")
                if len(parts) == 2: addr, port = parts[0], parts[1]
            if addr and port: return str(addr), str(port)
    except: pass
    return None, None

def get_country_boost(info):
    cfg = info.get("config", "").lower()
    search_text = cfg
    if cfg.startswith("vmess://"):
        try:
            b64 = cfg[8:] + "=" * ((4 - len(cfg[8:]) % 4) % 4)
            data = json.loads(base64.b64decode(b64).decode("utf-8", errors="ignore"))
            search_text += " " + str(data.get("ps", "")).lower()
        except: pass
    for country in PREFERRED_COUNTRIES:
        if country in search_text:
            return 250
    return 0

def calc_github_score(info):
    s, f = info.get("success", 0), info.get("fail", 0)
    hist = info.get("history", [])
    total = s + f
    if total == 0: return -1000.0
    if hist and hist[-1] == 9999: return 5.0
    
    base = (s / total) * 500
    recent = hist[-5:] if len(hist) >= 5 else hist
    if recent:
        ratio = sum(1 for x in recent if x < 9000) / len(recent)
        if ratio >= 0.8: base += 100
        elif ratio >= 0.6: base += 50
        elif ratio <= 0.2: base -= 150
        else: base -= 50
        
    valid = [x for x in hist if x < 9000]
    if valid:
        avg = sum(valid[-10:]) / len(valid[-10:])
        if avg < 150: base += 150
        elif avg < 300: base += 100
        elif avg < 500: base += 50
        
    return round(max(0, base + get_country_boost(info)), 2)

def check_api_ping(addr, port):
    try:
        time.sleep(0.2)
        payload = {"targets": [addr], "type": "ping", "locations": [{"country": "ae"}, {"country": "tr"}, {"country": "de"}], "limit": 3}
        res = requests.post("https://api.globalping.io/v1/measurements", json=payload, timeout=10)
        if res.status_code == 429:
            time.sleep(5)
            return check_api_ping(addr, port)
        if res.status_code != 201: return False, 0
        
        mid = res.json()["id"]
        for _ in range(10):
            time.sleep(1)
            data = requests.get(f"https://api.globalping.io/v1/measurements/{mid}", timeout=5).json()
            if data.get("status") == "finished":
                pings = [r["result"]["stats"]["avg"] for r in data.get("results", []) if r.get("result", {}).get("status") == "finished" and r["result"]["stats"].get("loss") == 0 and r["result"]["stats"].get("avg")]
                if pings: return True, sum(pings) / len(pings)
                return False, 0
        return False, 0
    except Exception:
        try:
            t0 = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((addr, int(port)))
            sock.close()
            return True, (time.time() - t0) * 1000
        except:
            return False, 0

def main():
    log("Loading DB...")
    with open("database/database.json", "r", encoding="utf-8") as f:
        db = json.load(f)
    
    log("Stage 1: Calculating GitHub + Country scores for ALL configs...")
    for h, info in db.items():
        info["github_score"] = calc_github_score(info)
        
    sorted_all = sorted(db.values(), key=lambda x: x.get("github_score", -1000), reverse=True)
    
    # حذف تکراری‌ها
    unique_configs = []
    seen = set()
    for cfg in sorted_all:
        cfg_str = cfg.get("config", "").strip()
        if cfg_str and cfg_str not in seen and cfg.get("github_score", -1000) > 10:
            seen.add(cfg_str)
            unique_configs.append(cfg)
            
    log(f"Total unique valid configs: {len(unique_configs)}")
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

    # ساخت فایل ویژه best_i.txt (مرحله ۲: تست API روی ۳۰۰ تای برتر)
    log("Stage 2: Running Multi-Region API on top 300 configs for best_i.txt...")
    top_300 = unique_configs[:300]
    premium_results = []
    
    def test_premium(info):
        addr, port = extract_addr_port(info.get("config", ""))
        if not addr or not port: return info, 0
        ok, ms = check_api_ping(addr, port)
        # امتیاز نهایی پریمیوم: اگر API اوکی بود ۵۰۰ + امتیاز کشور، وگرنه فقط امتیاز کشور
        final_score = (500 if ok else 0) + get_country_boost(info)
        return info, final_score

    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {ex.submit(test_premium, info): info for info in top_300}
        for future in as_completed(futures):
            info, score = future.result()
            info["premium_score"] = score
            premium_results.append(info)
            
    # مرتب‌سازی نهایی ۳۰۰ تای تست شده بر اساس امتیاز پریمیوم
    premium_results.sort(key=lambda x: x.get("premium_score", 0), reverse=True)
    
    # برداشتن دقیقاً ۱۰۰ تای برتر
    final_best_i = premium_results[:100]
    with open("output/best_i.txt", "w", encoding="utf-8") as f:
        for cfg in final_best_i:
            f.write(cfg.get("config", "") + "\n")
            
    log(f"👑 Wrote exactly {len(final_best_i)} ultra-stable configs to output/best_i.txt")
    log("✅ ALL files generated successfully!")

if __name__ == "__main__":
    main()
