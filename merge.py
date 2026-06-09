import requests

REPOS = ["AvenCores/goida-vpn-configs"]

def get_all_files(repo):
    url = f"https://api.github.com/repos/{repo}/git/trees/main?recursive=1"
    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        return []

    data = r.json()
    return data.get("tree", [])

def fetch(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.text
    except:
        pass
    return None

def is_config(text):
    if not text:
        return False

    t = text.lower()

    if "<html" in t:
        return False

    return any(k in t for k in ["vmess", "vless", "trojan", "ss://", "ssr://"])

def main():
    results = []
    seen = set()

    for repo in REPOS:
        files = get_all_files(repo)

        for f in files:
            if f.get("type") != "blob":
                continue

            path = f.get("path", "")

            if not any(ext in path for ext in [".txt", ".sub", ".json", ".yaml", ""]):
                continue

            raw_url = f"https://raw.githubusercontent.com/{repo}/main/{path}"

            content = fetch(raw_url)

            if is_config(content):
                if content not in seen:
                    seen.add(content)
                    results.append(content)

    with open("all.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print("Done:", len(results))

if __name__ == "__main__":
    main()
