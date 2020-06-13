from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

from . import passwords
from .decorators import require_password
from .utils import base64_encode, reverse


async def home(request: Request) -> PlainTextResponse:
    return PlainTextResponse(passwords.LEVEL_1)


@require_password(passwords.LEVEL_1)
async def level_1(request: Request) -> JSONResponse:
    """Return plain password for the next level."""

    return JSONResponse({"password": passwords.LEVEL_2})


@require_password(passwords.LEVEL_2)
async def level_2(request: Request) -> JSONResponse:
    """Return reversed password."""

    return JSONResponse({reverse("password"): reverse(passwords.LEVEL_3)})


@require_password(passwords.LEVEL_3)
async def level_3(request: Request) -> JSONResponse:
    """Return base64 encoded password."""

    return JSONResponse({"password": base64_encode(passwords.LEVEL_4)})


@require_password(passwords.LEVEL_4)
async def level_4(request: Request) -> JSONResponse:
    """Return fake password in body and real one in headers."""

    return JSONResponse(
        {"password": "qwerty"}, headers={"X-Real-Password": passwords.LEVEL_5}
    )


@require_password(passwords.LEVEL_5)
async def level_5(request: Request) -> JSONResponse:
    """Return plain password. Endpoint will be available only for DELETE method."""

    return JSONResponse({"password": passwords.LEVEL_6})
