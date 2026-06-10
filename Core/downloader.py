import requests
import time
from concurrent.futures import ThreadPoolExecutor
from Core.logger import log

DEFAULT_TIMEOUT = 20
RETRY_COUNT = 3
MAX_WORKERS = 10


def fetch_url(url):
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            r = requests.get(url, timeout=DEFAULT_TIMEOUT)

            if r.status_code == 200:
                return url, r.text

            log(f"[ERROR] {url} status={r.status_code}")

        except Exception as e:
            log(f"[ERROR] {url} -> {str(e)}")

        time.sleep(attempt * 2)

    return url, None


def download_sources(sources):
    results = {}

    if not sources:
        return results

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(fetch_url, url) for url in sources]

        for f in futures:
            url, content = f.result()

            if content:
                results[url] = content

    log(f"[DOWNLOAD DONE] success={len(results)} total={len(sources)}")

    return results
