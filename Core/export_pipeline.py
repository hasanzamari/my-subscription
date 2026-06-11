EXPORTS = []


def register(func):

    EXPORTS.append(func)


def run(context=None):

    for func in EXPORTS:

        try:

            func(context)

        except Exception:

            pass
