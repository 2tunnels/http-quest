from starlette.applications import Starlette
from starlette.routing import Route

from .endpoints import Home, Level1

routes = [
    Route("/", Home),
    Route("/level-1", Level1),
]

application = Starlette(routes=routes)
