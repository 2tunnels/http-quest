from starlette.applications import Starlette
from starlette.routing import Route

from .endpoints import home, level_1, level_2


def get_application() -> Starlette:
    routes = [
        Route("/", home),
        Route("/level-1", level_1),
        Route("/level-2", level_2),
    ]

    return Starlette(routes=routes)
