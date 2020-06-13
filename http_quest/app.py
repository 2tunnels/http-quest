from starlette.applications import Starlette
from starlette.routing import Route

from .endpoints import home, level_1, level_2, level_3


def get_application() -> Starlette:
    routes = [
        Route("/", home),
        Route("/level-1", level_1),
        Route("/level-2", level_2),
        Route("/level-3", level_3),
    ]

    return Starlette(routes=routes)
