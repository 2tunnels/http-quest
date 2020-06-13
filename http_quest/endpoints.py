from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

from . import passwords
from .decorators import require_password
from .utils import base64_encode, reverse


async def home(request: Request) -> PlainTextResponse:
    return PlainTextResponse(passwords.LEVEL_1)


@require_password(passwords.LEVEL_1)
async def level_1(request: Request) -> JSONResponse:
    """Return plain password for next level."""

    return JSONResponse({"password": passwords.LEVEL_2})


@require_password(passwords.LEVEL_2)
async def level_2(request: Request) -> JSONResponse:
    """Return reversed password for next level."""

    return JSONResponse({reverse("password"): reverse(passwords.LEVEL_3)})


@require_password(passwords.LEVEL_3)
async def level_3(request: Request) -> JSONResponse:
    """Return base64 encoded password for next level."""

    return JSONResponse({"password": base64_encode(passwords.LEVEL_4)})
