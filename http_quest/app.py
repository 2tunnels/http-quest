from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.routing import Mount, Route
from starlette_x_bugsnag.middleware import BugsnagMiddleware

from . import __version__, endpoints, levels, settings


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
                Route("/6", levels.user_agent, name="user_agent"),
                Route("/7", levels.accept_language, name="accept_language"),
                Route("/8", levels.redirect, name="redirect"),
                Route("/9", levels.robots, name="robots", methods=["POST"]),
                Route(
                    "/10", levels.guess_number, name="guess_number", methods=["POST"]
                ),
                Route("/11", levels.mask, name="mask", methods=["POST"]),
                Route("/12", levels.finish, name="finish"),
            ],
        ),
    ]

    release_stage = "development" if settings.DEBUG else "production"

    return Starlette(
        debug=settings.DEBUG,
        routes=routes,
        middleware=[
            Middleware(
                BugsnagMiddleware,
                api_key=str(settings.BUGSNAG_API_KEY),
                app_version=__version__,
                project_root=None,
                release_stage=release_stage,
            ),
        ],
    )
