from Core.best_manager import build_sets
from Core.export_best import write


def export(configs):

    sets = build_sets(configs)

    for name, items in sets.items():

        write(
            name,
            items
        )
