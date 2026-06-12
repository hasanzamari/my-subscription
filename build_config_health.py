import os

content = '''import json
import os
from datetime import datetime

FILE = "database/config_health.json"

def load():
    if not os.path.exists(FILE):
        return {}
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save(data):
    os.makedirs("database", exist_ok=True)
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_config_health(config_hash, success, latency=None, error_message=None):
    data = load()
    if config_hash not in data:
        data[config_hash] = {
            "success_count": 0,
            "failed_count": 0,
            "latency_history": [],
            "avg_latency": None,
            "last_test": None,
            "last_success": None,
            "last_error": None
        }
    config = data[config_hash]
    if success:
        config["success_count"] += 1
        config["last_success"] = datetime.now().isoformat()
        if latency is not None:
            config["latency_history"].append(latency)
            if len(config["latency_history"]) > 20:
                config["latency_history"] = config["latency_history"][-20:]
            config["avg_latency"] = sum(config["latency_history"]) / len(config["latency_history"])
    else:
        config["failed_count"] += 1
        config["last_error"] = error_message
    config["last_test"] = datetime.now().isoformat()
    save(data)
    return config

def sync_to_database(db_path="database/database.json"):
    try:
        if not os.path.exists(db_path):
            return 0
        with open(db_path, 'r', encoding='utf-8') as f:
            db = json.load(f)
        health_data = load()
        updated_count = 0
        for config_hash, health_info in health_data.items():
            if config_hash in db:
                db[config_hash]["success"] = health_info.get("success_count", 0)
                db[config_hash]["fail"] = health_info.get("failed_count", 0)
                history = health_info.get("latency_history", [])
                if history:
                    db[config_hash]["history"] = history
                updated_count += 1
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        return updated_count
    except Exception as e:
        print(f"Sync error: {e}")
        return 0
'''

os.makedirs("Core", exist_ok=True)
with open("Core/config_health.py", "w", encoding="utf-8") as f:
    f.write(content)
print("OK: Core/config_health.py created")
