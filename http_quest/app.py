from starlette.applications import Starlette
from starlette.routing import Route

from .endpoints import (
    home,
    level_1,
    level_2,
    level_3,
    level_4,
    level_5,
    level_6,
    level_7,
    level_8,
    level_9,
    level_10_entry,
    level_10_secret,
)


def get_application() -> Starlette:
    routes = [
        Route("/", home, name="home"),
        Route("/level-1", level_1, name="level_1"),
        Route("/level-2", level_2, name="level_2"),
        Route("/level-3", level_3, name="level_3"),
        Route("/level-4", level_4, name="level_4"),
        Route("/level-5", level_5, name="level_5", methods=["DELETE"]),
        Route("/level-6", level_6, name="level_6"),
        Route("/level-7", level_7, name="level_7"),
        Route("/level-8", level_8, name="level_8", methods=["POST"]),
        Route("/level-9", level_9, name="level_9"),
        Route("/level-10", level_10_entry, name="level_10_entry"),
        Route("/level-10/{secret}", level_10_secret, name="level_10_secret"),
    ]

    return Starlette(routes=routes)
