from Core.github_paths import COMMON_PATHS


BRANCHES = [
    "main",
    "master",
    "dev"
]


def build(owner, repo):

    urls = []

    for branch in BRANCHES:

        for path in COMMON_PATHS:

            urls.append(
                f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
            )

    return list(dict.fromkeys(urls))
