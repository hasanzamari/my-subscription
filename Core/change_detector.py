from Core.hash_cache import sha


def changed(url, content, cache):

    new_hash = sha(content)

    old_hash = cache.get(url)

    if old_hash == new_hash:
        return False

    cache[url] = new_hash

    return True
