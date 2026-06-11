def sort_cache(cache):

    cache.sort(

        key=lambda x: (

            x["score"],

            x["updated"]

        ),

        reverse=True

    )

    return cache
