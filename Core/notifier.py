import os, requests
from datetime import datetime
from Core.logger import log

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY", "hasanzamari/my-subscription")
REPORT_FILE = "reports/status_report.md"

def send_telegram_message(message):
    """ارسال پیام متنی به تلگرام"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        log("⚠️ Telegram credentials not set. Skipping notification.")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            log("📤 Status message sent to Telegram")
            return True
        else:
            log(f"❌ Telegram API error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        log(f"❌ Failed to send Telegram message: {e}")
        return False

def send_telegram_document(file_path, caption=""):
    """ارسال فایل به تلگرام به صورت Document"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    
    if not os.path.exists(file_path):
        log(f"⚠️ File not found: {file_path}")
        return False
    
    # بررسی حجم فایل (تلگرام حداکثر 50MB)
    file_size = os.path.getsize(file_path)
    if file_size > 50 * 1024 * 1024:
        log(f"⚠️ File too large ({file_size / 1024 / 1024:.1f}MB): {file_path}")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'document': (os.path.basename(file_path), f)}
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'caption': caption,
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, files=files, data=data, timeout=60)
            
        if response.status_code == 200:
            log(f"📤 File sent: {os.path.basename(file_path)}")
            return True
        else:
            log(f"❌ Failed to send file {file_path}: {response.status_code}")
            return False
    except Exception as e:
        log(f"❌ Error sending file {file_path}: {e}")
        return False

def build_raw_link(filename):
    """ساخت لینک Raw برای یک فایل"""
    return f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/output/{filename}"

def check_health(db, sources_count, new_configs_count):
    """بررسی سلامت و ارسال گزارش کامل + فایل‌ها به تلگرام"""
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    
    total = len(db)
    # فقط کانفیگ‌هایی که حداقل یک بار تست شده‌اند را در محاسبه سلامت در نظر بگیر
    tested_configs = [i for i in db.values() if (i.get("success", 0) + i.get("fail", 0)) > 0]
    
    if len(tested_configs) > 0:
        active = sum(1 for i in tested_configs if i.get("success", 0) > i.get("fail", 0))
        rate = (active / len(tested_configs) * 100)
        health_str = f"{rate:.1f}%"
    else:
        health_str = "Untested (Pending Nightly Test)"
    
    # لیست فایل‌های خروجی برای ارسال
    output_files = {
        "rotation_500.txt": "🔄 500 Rotating Configs",
        "best_iran.txt": "🇮🇷 Iran Optimized",
        "best_i.txt": "👑 Premium Top 100",
        "subscription_base64.txt": "🔐 Base64 (v2rayNG)",
        "singbox.json": "📱 Sing-Box (Hiddify)",
        "clash_meta.yaml": "⚔️ Clash Meta",
        "best_vless.txt": "🔹 VLESS Protocol",
        "best_trojan.txt": "🔻 Trojan Protocol",
        "best_reality.txt": "🛡️ Reality Protocol",
    }
    
    file_counts = {}
    for fname, label in output_files.items():
        fpath = f"output/{fname}"
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                if fname.endswith(".json") or fname.endswith(".yaml"):
                    count = "File"
                else:
                    count = str(len([l for l in f if l.strip()]))
                file_counts[fname] = {"label": label, "count": count, "path": fpath}
        else:
            file_counts[fname] = {"label": label, "count": "—", "path": None}
    
    # بررسی مشکلات
    issues = []
    if new_configs_count == 0: issues.append("⚠️ No new configs added")
    if sources_count < 5: issues.append("⚠️ Low sources (<5)")
    if rate < 50: issues.append(f"⚠️ Low health: {rate:.1f}%")
    
    # ساخت پیام تلگرام
    status_emoji = "✅" if not issues else "⚠️"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    
    msg = f"{status_emoji} *Smart Subscription Update*\n"
    msg += f"🕐 _{now_str}_\n\n"
    msg += f"📊 *Stats:*\n"
    msg += f"├ Total: `{total}`\n"
    msg += f"├ Active: `{active}`\n"
    msg += f"├ Health: `{rate:.1f}%`\n"
    msg += f"├ Sources: `{sources_count}`\n"
    msg += f"└ New: `{new_configs_count}`\n\n"
    
    msg += f"📥 *Quick Links:*\n"
    for fname, info in file_counts.items():
        link = build_raw_link(fname)
        count_str = f" ({info['count']})" if info['count'] != "—" else ""
        msg += f"{info['label']}{count_str}\n"
        msg += f"└ [Open Raw]({link})\n"
    
    if issues:
        msg += f"\n🚨 *Alerts:*\n"
        for issue in issues:
            msg += f"{issue}\n"
    
    msg += f"\n📎 _Files attached below_"
    
    # ذخیره گزارش محلی
    local_report = msg.replace("*", "").replace("_", "").replace("[Open Raw](", "").replace(")", "")
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(local_report)
    
    log(f"📋 Report saved to {REPORT_FILE}")
    
    # ارسال پیام متنی
    send_telegram_message(msg)
    
    # ✅ ارسال فایل‌های مهم به صورت Document
    files_to_send = [
        "rotation_500.txt",
        "best_iran.txt", 
        "best_i.txt",
        "subscription_base64.txt",
        "singbox.json",
        "clash_meta.yaml"
    ]
    
    sent_count = 0
    for fname in files_to_send:
        fpath = f"output/{fname}"
        if os.path.exists(fpath):
            info = file_counts.get(fname, {})
            caption = f"{info.get('label', fname)}\nCount: {info.get('count', 'N/A')}\n🕐 {now_str}"
            if send_telegram_document(fpath, caption):
                sent_count += 1
    
    log(f"📎 Sent {sent_count} files to Telegram")
    
    return len(issues) == 0

if __name__ == "__main__":
    test_db = {
        "h1": {"success": 10, "fail": 2},
        "h2": {"success": 5, "fail": 5},
    }
    check_health(test_db, 10, 100)
