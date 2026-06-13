import requests, os, time, re
from datetime import datetime
from Core.logger import log

SOURCES_FILE = "Sources/sources.txt"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")

def search_github_repos():
    """جستجوی ریپازیتوری‌های جدید v2ray در گیت‌هاب"""
    query = "v2ray subscription in:name,description"
    url = f"https://api.github.com/search/repositories?q={query}&sort=updated&order=desc&per_page=30"
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            repos = response.json().get("items", [])
            return [repo["html_url"] for repo in repos]
        else:
            log(f"⚠️ GitHub API error: {response.status_code}")
    except Exception as e:
        log(f"❌ GitHub API error: {e}")
    
    return []

def extract_sub_urls(repo_url):
    """استخراج لینک‌های ساب از یک ریپازیتوری"""
    # تبدیل لینک ریپازیتوری به لینک Raw
    repo_url = repo_url.replace("github.com", "raw.githubusercontent.com")
    repo_url = repo_url.replace("https://raw.githubusercontent.com/", "")
    
    parts = repo_url.split("/")
    if len(parts) < 2:
        return []
    
    owner, repo = parts[0], parts[1]
    base_url = f"https://raw.githubusercontent.com/{owner}/{repo}"
    
    # مسیرهای احتمالی فایل ساب
    possible_paths = [
        "/main/sub.txt",
        "/main/Sub.txt",
        "/master/sub.txt",
        "/master/Sub.txt",
        "/main/merged/base64",
        "/main/sub/vmess",
        "/main/sub/vless",
        "/main/sub/trojan",
        "/main/sub/ss",
        "/main/all.txt",
        "/main/configs.txt",
        "/main/v2ray.txt",
    ]
    
    valid_urls = []
    for path in possible_paths:
        full_url = base_url + path
        try:
            response = requests.head(full_url, timeout=5)
            if response.status_code == 200:
                valid_urls.append(full_url)
        except:
            pass
    
    return valid_urls

def discover_new_sources():
    """کشف و اضافه کردن منابع جدید"""
    if not os.path.exists(SOURCES_FILE):
        os.makedirs(os.path.dirname(SOURCES_FILE), exist_ok=True)
        with open(SOURCES_FILE, 'w', encoding='utf-8') as f:
            f.write('')
    
    with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
        existing_urls = set(line.strip() for line in f if line.strip())
    
    log("🔍 Searching GitHub for new v2ray repositories...")
    repos = search_github_repos()
    
    if not repos:
        log("⚠️ No new repositories found")
        return 0
    
    new_urls = set()
    for repo in repos[:10]:  # فقط 10 ریپازیتوری برتر
        sub_urls = extract_sub_urls(repo)
        new_urls.update(sub_urls)
        time.sleep(0.5)  # جلوگیری از Rate Limit
    
    # حذف لینک‌های تکراری
    urls_to_add = new_urls - existing_urls
    
    if urls_to_add:
        with open(SOURCES_FILE, 'a', encoding='utf-8') as f:
            for url in urls_to_add:
                f.write(url + '\n')
        log(f"✅ Auto-Discovery: Added {len(urls_to_add)} new sources from GitHub")
    else:
        log("ℹ️ No new sources discovered")
    
    return len(urls_to_add)

if __name__ == "__main__":
    discover_new_sources()
