from Core.github_queries import QUERIES


def build():

    urls = []

    for q in QUERIES:

        q = q.replace(" ", "+")

        urls.append(

            f"https://github.com/search?q={q}&type=code"

        )

    return urls
