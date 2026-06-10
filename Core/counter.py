from Core.protocol_detector import detect


def count(configs):

    result = {}

    for c in configs:

        p = detect(c)

        result[p] = result.get(p, 0) + 1

    return result
