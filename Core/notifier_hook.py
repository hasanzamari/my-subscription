HOOKS = []


def register(func):

    HOOKS.append(func)


def execute(context):

    for hook in HOOKS:

        try:

            hook(context)

        except Exception:

            pass
