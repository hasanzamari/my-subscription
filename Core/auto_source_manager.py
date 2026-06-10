from Core.source_repository import add
from Core.source_discovery import discover


def process(raw_sources):

    added = 0

    for content in raw_sources.values():

        urls = discover(content)

        for url in urls:

            if add(url):
                added += 1

    return added
