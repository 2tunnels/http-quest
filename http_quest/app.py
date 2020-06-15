from starlette.applications import Starlette
from starlette.routing import Mount, Route

from . import endpoints, levels


def get_application() -> Starlette:
    routes = [
        Route("/", endpoints.home, name="home"),
        Route("/robots.txt", endpoints.robots, name="robots"),
        Mount(
            "/level",
            name="level",
            routes=[
                Route("/1", levels.plain, name="plain"),
                Route("/2", levels.reverse, name="reverse"),
                Route("/3", levels.base64, name="base64"),
                Route("/4", levels.header, name="header"),
                Route("/5", levels.delete, name="delete", methods=["DELETE"]),
                Route("/6", levels.redirect, name="redirect"),
                Route("/7", levels.user_agent, name="user_agent"),
                Route("/8", levels.guess_number, name="guess_number", methods=["POST"]),
                Route("/9", levels.accept_language, name="accept_language"),
                Route("/10", levels.mask, name="mask", methods=["POST"]),
                Route("/11", levels.robots, name="robots", methods=["POST"]),
            ],
        ),
    ]

    return Starlette(routes=routes)
