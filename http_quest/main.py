from starlette.applications import Starlette
from starlette.routing import Route

from .endpoints import Home, Level1, Level2

routes = [
    Route("/", Home),
    Route("/level-1", Level1),
    Route("/level-2", Level2),
]

application = Starlette(routes=routes)
