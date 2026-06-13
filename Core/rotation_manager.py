import os
from Core.logger import log

SOURCE_FILE = "output/best_iran.txt"
OUTPUT_FILE = "output/rotation_500.txt"
STATE_FILE = "database/rotation_index.txt" # این فایل ایندکس را ذخیره می‌کند
CHUNK_SIZE = 500

def rotate_configs():
    if not os.path.exists(SOURCE_FILE):
        log("⚠️ best_iran.txt not found. Skipping rotation.")
        return

    # ۱. خواندن کانفیگ‌های خوب (این فایل از قبل مرتب و بهینه شده است)
    with open(SOURCE_FILE, "r", encoding="utf-8") as f:
        configs = [line.strip() for line in f if line.strip()]

    total_configs = len(configs)
    if total_configs == 0:
        log("⚠️ No configs in best_iran.txt")
        return

    # ۲. خواندن ایندکس قبلی (از کجا باید شروع کنیم؟)
    current_index = 0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                current_index = int(f.read().strip())
        except:
            current_index = 0

    # ۳. محاسبه برش جدید
    start_idx = current_index % total_configs
    end_idx = start_idx + CHUNK_SIZE

    # اگر به انتهای لیست رسیدیم و ۵۰۰ تا کم بود، از اول شروع کن تا فایل همیشه ۵۰۰ تایی باشد
    if end_idx > total_configs:
        start_idx = 0
        end_idx = CHUNK_SIZE
        log("🔄 Reached end of list. Resetting rotation to 0.")

    selected_configs = configs[start_idx:end_idx]
    
    # ۴. ذخیره فایل خروجی ۵۰۰ تایی
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for cfg in selected_configs:
            f.write(cfg + "\n")

    # ۵. به‌روزرسانی ایندکس برای دور بعدی (۶ ساعت بعد)
    next_index = (start_idx + CHUNK_SIZE) % total_configs
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(str(next_index))

    log(f"✅ Rotation successful: Extracted {len(selected_configs)} configs (Index {start_idx} to {end_idx-1}) to {OUTPUT_FILE}")

if __name__ == "__main__":
    rotate_configs()
