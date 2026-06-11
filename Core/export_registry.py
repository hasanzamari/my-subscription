REGISTRY = {}


def register(name, func):

    REGISTRY[name] = func


def get():

    return REGISTRY
