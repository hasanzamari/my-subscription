import json, os, time, subprocess, re, base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from Core.logger import log

DB_FILE = "database/database.json"
HEALTH_FILE = "database/config_health.json"
WORKERS = 50
TIMEOUT = 3
CHUNK = 3000

def extract_addr(cfg):
    try:
        cfg = cfg.strip()
        if cfg.startswith("vmess://"):
            return json.loads(base64.b64decode(cfg[8:]).decode()).get("add")
        for p in ["vless://", "trojan://", "ss://", "hy2://", "hysteria://", "tuic://"]:
            if cfg.startswith(p):
                m = re.search(rf'{re.escape(p)}[^@]+@([^:]+):', cfg)
                if m: return m.group(1)
        if cfg.startswith("ssr://"):
            return base64.b64decode(cfg[6:]).decode().split(":")[0]
    except: pass
    return None

def ping(addr):
    try:
        t0 = time.time()
        r = subprocess.run(["ping", "-c", "1", "-W", str(TIMEOUT), addr], capture_output=True, text=True, timeout=TIMEOUT+2)
        ms = (time.time() - t0) * 1000
        if r.returncode == 0:
            m = re.search(r'time[=<](\d+\.?\d*)', r.stdout)
            if m: ms = float(m.group(1))
            return True, ms, None
        return False, None, "fail"
    except: return False, None, "timeout"

def worker(args):
    h, info = args
    cfg = info.get("config", "")
    addr = extract_addr(cfg)
    if not addr: return h, False, None, "no_addr"
    ok, ms, err = ping(addr)
    return h, ok, ms, err

def main():
    if not os.path.exists(DB_FILE): 
        return log("DB not found")
    
    with open(DB_FILE, "r", encoding="utf-8") as f:         db = json.load(f)
    
    cutoff = datetime.now() - timedelta(hours=24)
    untested = []
    for h, info in db.items():
        lt = info.get("last_test")
        if not lt:
            untested.append((h, info))
        else:
            try:
                if datetime.fromisoformat(lt) < cutoff:
                    untested.append((h, info))
            except: 
                untested.append((h, info))
    
    targets = untested[:CHUNK]
    log(f"Testing {len(targets)} configs (parallel={WORKERS})...")
    
    ok_cnt, fail_cnt, avg_ms = 0, 0, 0.0
    health_db = json.load(open(HEALTH_FILE, "r", encoding="utf-8")) if os.path.exists(HEALTH_FILE) else {}
    
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(worker, t): t[0] for t in targets}
        for f in as_completed(futs):
            h, ok, ms, err = f.result()
            now = datetime.now().isoformat()
            
            db[h]["last_test"] = now
            entry = health_db.get(h, {"success": 0, "fail": 0, "history": [], "last_test": None})
            entry["last_test"] = now
            
            if ok:
                ok_cnt += 1
                avg_ms += ms if ms else 0
                entry["success"] += 1
                if ms: 
                    entry["history"].append(ms)
                    if len(entry["history"]) > 30: 
                        entry["history"] = entry["history"][-30:]
            else:
                fail_cnt += 1
                entry["fail"] += 1
            
            health_db[h] = entry
    
    if ok_cnt: avg_ms /= ok_cnt
    log(f"Done: {ok_cnt} OK, {fail_cnt} FAIL. Avg: {avg_ms:.1f}ms")
    
    with open(DB_FILE, "w", encoding="utf-8") as f: 
        json.dump(db, f, indent=2, ensure_ascii=False)    with open(HEALTH_FILE, "w", encoding="utf-8") as f: 
        json.dump(health_db, f, indent=2, ensure_ascii=False)

if __name__ == "__main__": 
    main()
