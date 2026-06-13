import os
from datetime import datetime
from Core.logger import log

REPORT_FILE = "reports/status_report.md"

def check_health(db, sources_count, new_configs_count):
    """بررسی سلامت سیستم و تولید گزارش"""
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    
    total_configs = len(db)
    active_configs = sum(1 for info in db.values() if info.get("success", 0) > info.get("fail", 0))
    
    # محاسبه نرخ سلامت
    health_rate = (active_configs / total_configs * 100) if total_configs > 0 else 0
    
    # تشخیص مشکلات
    issues = []
    if new_configs_count == 0:
        issues.append("⚠️ No new configs added (sources may be down)")
    if sources_count < 5:
        issues.append("⚠️ Low number of sources (< 5)")
    if health_rate < 50:
        issues.append(f"⚠️ Low health rate: {health_rate:.1f}%")
    
    # تولید گزارش
    report = f"# 📊 Status Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    report += f"## 📈 Statistics\n"
    report += f"- **Total Configs:** `{total_configs}`\n"
    report += f"- **Active Configs:** `{active_configs}`\n"
    report += f"- **Health Rate:** `{health_rate:.1f}%`\n"
    report += f"- **Sources Count:** `{sources_count}`\n"
    report += f"- **New Configs Added:** `{new_configs_count}`\n\n"
    
    if issues:
        report += f"## ⚠️ Issues Detected\n"
        for issue in issues:
            report += f"- {issue}\n"
    else:
        report += f"## ✅ System Status: Healthy\n"
        report += f"All systems are operating normally.\n"
    
    # ذخیره گزارش
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    log(f"📋 Status report generated: {REPORT_FILE}")
    
    # اگر مشکل جدی وجود دارد، در لاگ هشدار بده
    if issues:
        for issue in issues:
            log(f"🚨 {issue}")
    
    return len(issues) == 0

if __name__ == "__main__":
    # تست
    test_db = {
        "hash1": {"success": 10, "fail": 2},
        "hash2": {"success": 5, "fail": 5},
    }
    check_health(test_db, 10, 100)
