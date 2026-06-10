import re
from Core.source_validator import valid_source

URL_PATTERN = re.compile(
    r"https?://[^\s\"'<>]+"
)


def discover(text):

    found = set()

    if not text:
        return found

    urls = URL_PATTERN.findall(text)

    for url in urls:

        if valid_source(url):
            found.add(url)

    return found
