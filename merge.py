import requests
from bs4 import BeautifulSoup

MAIN_REPO = "https://github.com/AvenCores/goida-vpn-configs"

def get_repo_links():
    try:
        r = requests.get(MAIN_REPO, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        links = set()

        for a in soup.find_all("a"):
            href = a.get("href")
            if href and "/tree/main" in href:
                full = "https://github.com" + href
                links.add(full)

        return list(links)

    except:
        return []

def convert_to_raw(repo_url):
    try:
        # تبدیل GitHub repo page به raw txt guess
        if "github.com" in repo_url:
            raw = repo_url.replace("github.com", "raw.githubusercontent.com")
            raw = raw.replace("/tree/main", "/main")
            return raw + "/README.md"
    except:
        pass
    return None

def fetch(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.text
    except:
        pass
    return None

def main():
    repos = get_repo_links()

    results = []
    seen = set()

    for repo in repos:
        raw = convert_to_raw(repo)
        if not raw:
            continue

        content = fetch(raw)
        if content and len(content) > 20:
            if content not in seen:
                seen.add(content)
                results.append(content)

    with open("all.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"Done: {len(results)} items")

if __name__ == "__main__":
    main()
