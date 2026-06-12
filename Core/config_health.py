"""
مدیریت سلامت کانفیگ‌ها
این ماژول اطلاعات تست و عملکرد هر کانفیگ رو ذخیره و بازیابی می‌کنه
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List

FILE = "database/config_health.json"


def load() -> Dict[str, Any]:
    """بارگذاری اطلاعات سلامت کانفیگ‌ها از فایل"""
    if not os.path.exists(FILE):
        return {}
    
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, IOError):
        return {}


def save(data: Dict[str, Any]) -> bool:
    """ذخیره اطلاعات سلامت کانفیگ‌ها در فایل"""
    try:
        os.makedirs("database", exist_ok=True)
        
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except IOError as e:
        print(f"❌ خطا در ذخیره فایل سلامت کانفیگ‌ها: {e}")
        return False


def update_config_health(
    config_hash: str,
    success: bool,
    latency: Optional[float] = None,
    error_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    به‌روزرسانی اطلاعات سلامت یک کانفیگ خاص
    
    Args:        config_hash: هش SHA256 کانفیگ
        success: آیا تست موفقیت‌آمیز بود؟
        latency: زمان پاسخ (میلی‌ثانیه) - اختیاری
        error_message: پیام خطا - اختیاری
        
    Returns:
        Dict: اطلاعات به‌روزرسانی شده کانفیگ
    """
    data = load()
    
    # اگر کانفیگ قبلاً وجود نداره، ساختار اولیه رو بساز
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
    
    # به‌روزرسانی شمارنده‌ها
    if success:
        config["success_count"] += 1
        config["last_success"] = datetime.now().isoformat()
        
        # به‌روزرسانی latency اگر ارائه شده باشه
        if latency is not None:
            # نگهداری فقط 20 تست آخر برای history
            config["latency_history"].append(latency)
            if len(config["latency_history"]) > 20:
                config["latency_history"] = config["latency_history"][-20:]
            
            # محاسبه میانگین
            config["avg_latency"] = sum(config["latency_history"]) / len(config["latency_history"])
    else:
        config["failed_count"] += 1
        config["last_error"] = error_message
    
    # به‌روزرسانی زمان آخرین تست
    config["last_test"] = datetime.now().isoformat()
    
    # ذخیره تغییرات
    save(data)
    
    return config

def get_config_health(config_hash: str) -> Optional[Dict[str, Any]]:
    """دریافت اطلاعات سلامت یک کانفیگ خاص"""
    data = load()
    return data.get(config_hash)


def get_all_health() -> Dict[str, Any]:
    """دریافت اطلاعات سلامت تمام کانفیگ‌ها"""
    return load()


def sync_to_database(db_path: str = "database/database.json") -> int:
    """
    همگام‌سازی اطلاعات سلامت با دیتابیس اصلی
    
    این تابع اطلاعات config_health.json رو به database.json منتقل می‌کنه
    تا scoring.py و best_manager.py بتونن از اون استفاده کنن
    
    Args:
        db_path: مسیر فایل database.json
        
    Returns:
        int: تعداد کانفیگ‌های به‌روزرسانی شده
    """
    try:
        # بارگذاری database.json
        if not os.path.exists(db_path):
            print(f"❌ فایل دیتابیس پیدا نشد: {db_path}")
            return 0
        
        with open(db_path, 'r', encoding='utf-8') as f:
            db = json.load(f)
        
        # بارگذاری config_health.json
        health_data = load()
        
        updated_count = 0
        
        # به‌روزرسانی هر کانفیگ در database
        for config_hash, health_info in health_data.items():
            if config_hash in db:
                db[config_hash]["success"] = health_info.get("success_count", 0)
                db[config_hash]["fail"] = health_info.get("failed_count", 0)
                
                # اضافه کردن history برای scoring.py
                history = health_info.get("latency_history", [])
                if history:
                    db[config_hash]["history"] = history
                                updated_count += 1
        
        # ذخیره database.json
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {updated_count} کانفیگ در database.json به‌روزرسانی شد")
        return updated_count
        
    except Exception as e:
        print(f"❌ خطا در همگام‌سازی: {e}")
        return 0


if __name__ == "__main__":
    print("🔧 تست ماژول سلامت کانفیگ...")
    
    # تست اضافه کردن چند کانفیگ نمونه
    test_configs = [
        ("hash_1", True, 150.5),
        ("hash_1", True, 145.2),
        ("hash_1", False, None),
        ("hash_2", True, 200.0),
        ("hash_2", True, 195.5),
        ("hash_3", True, 100.0),
        ("hash_3", True, 95.0),
        ("hash_3", True, 105.0),
    ]
    
    for config_hash, success, latency in test_configs:
        update_config_health(config_hash, success, latency)
        print(f"✓ به‌روزرسانی شد: {config_hash} - {'موفق' if success else 'ناموفق'}")
    
    print("\n📊 همگام‌سازی با database.json...")
    sync_to_database()
