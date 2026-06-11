from Core.export_registry import get


def run(context=None):

    exports = get()

    for _, func in exports.items():

        try:

            func(context)

        except Exception:

            pass
