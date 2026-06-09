import requests

# لینک اصلی که لیست repo ها داخلشه
SOURCE_LIST_URL = "https://raw.githubusercontent.com/hasanzamari/my-subscription/main/sources.txt"

def extract_urls():
    try:
        r = requests.get(SOURCE_LIST_URL, timeout=10)
        lines = r.text.splitlines()
        return [x.strip() for x in lines if x.strip()]
    except:
        return []

def fetch_content(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.text
    except:
        pass
    return None

def is_valid(text):
    if not text:
        return False
    if len(text) < 10:
        return False
    return True

def main():
    urls = extract_urls()

    results = []
    seen = set()

    for url in urls:
        content = fetch_content(url)

        if is_valid(content):
            if content not in seen:
                seen.add(content)
                results.append(content)

    with open("all.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"Done. {len(results)} configs saved.")

if __name__ == "__main__":
    main()
