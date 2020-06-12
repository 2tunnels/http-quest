from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

from . import passwords
from .decorators import require_password


class Home(HTTPEndpoint):
    @staticmethod
    async def get(request: Request) -> PlainTextResponse:
        return PlainTextResponse(passwords.LEVEL_1)


class Level1(HTTPEndpoint):
    @require_password(passwords.LEVEL_1)
    async def get(self, request: Request) -> JSONResponse:
        return JSONResponse({"password": "foobar"})
