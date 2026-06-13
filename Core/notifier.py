import os, requests
from datetime import datetime
from Core.logger import log

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
REPORT_FILE = "reports/status_report.md"

def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
        log("📤 Alert sent to Telegram")
    except: pass

def check_health(db, sources_count, new_configs_count):
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    total = len(db)
    active = sum(1 for i in db.values() if i.get("success", 0) > i.get("fail", 0))
    rate = (active / total * 100) if total > 0 else 0
    
    issues = []
    if new_configs_count == 0: issues.append("⚠️ هیچ کانفیگ جدیدی اضافه نشد")
    if sources_count < 5: issues.append("⚠️ تعداد منابع کم است (<5)")
    if rate < 50: issues.append(f"⚠️ نرخ سلامت پایین: {rate:.1f}%")
    
    report = f"# 📊 Status - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    report += f"- کل: `{total}` | فعال: `{active}` | سلامت: `{rate:.1f}%`\n"
    report += f"- منابع: `{sources_count}` | جدید: `{new_configs_count}`\n"
    if issues: report += "\n" + "\n".join(issues)
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f: f.write(report)
    log("📋 Report saved")
    
    if issues:
        alert = "🚨 **هشدار سیستم ساب‌اسکریپشن**\n\n" + "\n".join(issues)
        send_telegram_alert(alert)
