from Core.notifier_registry import run
from Core.notifier_context import build


def notify(
    files,
    stats
):

    context = build(
        files,
        stats
    )

    run(context)
