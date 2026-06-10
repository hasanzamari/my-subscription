from Core.github_queries import QUERIES


def build():

    searches = []

    for q in QUERIES:

        q = q.replace(" ", "+")

        searches.append(
            f"https://github.com/search?q={q}&type=repositories"
        )

        searches.append(
            f"https://github.com/search?q={q}&type=code"
        )

    return list(dict.fromkeys(searches))
