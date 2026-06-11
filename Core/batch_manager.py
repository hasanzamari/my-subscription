def batches(items, size=200):

    for i in range(

        0,

        len(items),

        size

    ):

        yield items[

            i:i + size

      ]
