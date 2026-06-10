import re
from Core.source_validator import valid_source

PATTERN = re.compile(
    r'https?://[^\s<>"\'\)\]]+'
)


def discover(text):

    result = set()

    if not text:
        return result

    for url in PATTERN.findall(text):

        url = url.strip()

        if "github.com" in url and "/blob/" in url:

            url = url.replace(
                "github.com",
                "raw.githubusercontent.com"
            )

            url = url.replace(
                "/blob/",
                "/"
            )

        if valid_source(url):

            result.add(url)

    return result
