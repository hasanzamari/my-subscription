import json, os, time, subprocess, re, base64
from datetime import datetime
from Core import config_health
from Core.logger import log
DB_FILE = "database/database.json"
MAX_CONFIGS = 200
def extract_server_address(config):
    try:
        config = config.strip()
        if config.startswith("vmess://"):
            try: return json.loads(base64.b64decode(config[8:]).decode('utf-8')).get("add")
            except: pass
        if config.startswith("vless://") or config.startswith("trojan://") or config.startswith("ss://"):
            match = re.search(r'://[^@]+@([^:]+):', config)
            if match: return match.group(1)
        if config.startswith("ssr://"):
            try: return base64.b64decode(config[6:]).decode('utf-8').split(':')[0]
            except: pass
        for p in ["hy2://", "hysteria://", "tuic://"]:
            if config.startswith(p):
                match = re.search(rf'{re.escape(p)}[^@]+@([^:]+):', config)
                if match: return match.group(1)
        return None
    except Exception as e:
        return None
def ping_server(address, timeout=5):
    try:
        start = time.time()
        result = subprocess.run(["ping", "-c", "1", "-W", str(timeout), address], capture_output=True, text=True, timeout=timeout + 2)
        latency = (time.time() - start) * 1000
        if result.returncode == 0:
            match = re.search(r'time[=<](\d+\.?\d*)', result.stdout)
            if match: latency = float(match.group(1))
            return True, latency, None
        return False, None, "Ping failed"
    except:
        return False, None, "Timeout"
def test_single_config(config_hash, config_str):
    address = extract_server_address(config_str)
    if not address: return False, None, "No address"
    return ping_server(address)
def test_all_configs(db_path=DB_FILE, max_configs=MAX_CONFIGS, sync_db=True):
    try:
        if not os.path.exists(db_path): return {"error": "DB not found"}
        with open(db_path, 'r', encoding='utf-8') as f: db = json.load(f)
        log(f"Testing {min(len(db), max_configs)} configs...")
        success_count, failed_count, total_latency, tested = 0, 0, 0.0, 0
        for config_hash, info in list(db.items())[:max_configs]:
            config_str = info.get("config", "")
            if not config_str: continue
            tested += 1
            success, latency, error = test_single_config(config_hash, config_str)
            config_health.update_config_health(config_hash=config_hash, success=success, latency=latency, error_message=error)
            if success:
                log(f"[{tested}] OK ({latency:.1f}ms)")
                success_count += 1
                if latency: total_latency += latency
            else:
                log(f"[{tested}] FAIL ({error})")
                failed_count += 1
        avg_latency = total_latency / success_count if success_count > 0 else 0
        if sync_db: config_health.sync_to_database(db_path)
        log(f"Done: {success_count} OK, {failed_count} FAIL. Avg: {avg_latency:.1f}ms")
        return {"success": success_count, "failed": failed_count, "tested": tested}
    except Exception as e:
        log(f"Error: {e}")
        return {"error": str(e)}
if __name__ == "__main__":
    log("Starting config tests...")
    test_all_configs()
