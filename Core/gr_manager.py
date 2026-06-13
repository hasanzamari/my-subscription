import os
import hashlib
from Core.logger import log

SOURCE_FILE = "output/best_iran.txt"
OUTPUT_FILE = "output/best_GR.txt"
STATE_FILE = "database/gr_rotation_index.txt"
CHUNK_SIZE = 300  # تعداد کانفیگ آلمان در هر بار استخراج (قابل تغییر)

def is_germany(cfg):
    """بررسی اینکه آیا کانفیگ مربوط به آلمان است یا خیر"""
    cfg_lower = cfg.lower()
    gr_keywords = ['de', '🇩🇪', 'germany', 'frankfurt', 'آلمان', 'german', 'berlin', 'de-']
    return any(kw in cfg_lower for kw in gr_keywords)

def manage_gr_configs():
    if not os.path.exists(SOURCE_FILE):
        log("⚠️ best_iran.txt not found. Skipping GR extraction.")
        return

    # ۱. خواندن و فیلتر کردن کانفیگ‌های آلمان
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        all_configs = [line.strip() for line in f if line.strip()]

    gr_configs = [cfg for cfg in all_configs if is_germany(cfg)]
    
    # ۲. حذف تکراری‌های داخلی (بر اساس اثر انگشت SHA-256)
    unique_gr_configs = []
    seen_hashes = set()
    for cfg in gr_configs:
        cfg_hash = hashlib.sha256(cfg.encode('utf-8')).hexdigest()
        if cfg_hash not in seen_hashes:
            seen_hashes.add(cfg_hash)
            unique_gr_configs.append(cfg)

    total_gr = len(unique_gr_configs)
    if total_gr == 0:
        log("⚠️ No Germany configs found in best_iran.txt")
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
        return

    # ۳. خواندن ایندکس قبلی (برای جلوگیری از تکرار در دورهای بعدی)
    current_index = 0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                current_index = int(f.read().strip())
        except:
            current_index = 0

    # ۴. محاسبه برش جدید
    start_idx = current_index % total_gr
    end_idx = start_idx + CHUNK_SIZE

    # اگر به انتهای لیست رسیدیم، از اول شروع کن
    if end_idx > total_gr:
        start_idx = 0
        end_idx = min(CHUNK_SIZE, total_gr)
        log("🔄 Reached end of Germany configs list. Resetting rotation to 0.")

    selected_configs = unique_gr_configs[start_idx:end_idx]
    
    # ۵. ذخیره فایل خروجی
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for cfg in selected_configs:
            f.write(cfg + "\n")

    # ۶. به‌روزرسانی ایندکس برای ۱۲ ساعت بعد
    next_index = (start_idx + CHUNK_SIZE) % total_gr
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(str(next_index))

    log(f"✅ GR Extraction successful: Extracted {len(selected_configs)} Germany configs (Index {start_idx} to {end_idx-1}) to {OUTPUT_FILE}")

if __name__ == "__main__":
    manage_gr_configs()
