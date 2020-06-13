from typing import Union

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
from starlette.status import HTTP_400_BAD_REQUEST

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


@require_password(passwords.LEVEL_6)
async def level_6(request: Request) -> Union[RedirectResponse, JSONResponse]:
    """Return plain password if user follows redirect chain."""

    chain_of_secrets = [
        "itR6F7k4EA",
        "sNbQSNNMjQ",
        "8kwWsi3pos",
        "OGNqhAqqKR",
        "EQBJeRAjgZ",
        "1ISDOG1PmQ",
        "E1mlttngnT",
        "TdEW5CQfaD",
        "WECCgzfBg3",
        "D27AChlgXU",
        "aZsQKifS73",
        "d6B8h2m0WV",
        "NBzxKHhqf7",
        "a1pgijek8d",
        "z2K6Y09o0D",
        "n3ghhMg9Vk",
        "gIGp1dhqVp",
        "lZMctcrR0u",
        "aXdbPBjCRX",
        "lKTGjukENC",
    ]

    secret = request.query_params.get("secret", "")

    if not secret:
        redirect_url = request.url_for("level_6") + "?secret=" + chain_of_secrets[0]
        return RedirectResponse(redirect_url)

    try:
        index = chain_of_secrets.index(secret)
    except ValueError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Wrong secret")

    try:
        next_secret = chain_of_secrets[index + 1]
    except IndexError:
        return JSONResponse({"password": passwords.LEVEL_7})

    redirect_url = request.url_for("level_6") + "?secret=" + next_secret

    return RedirectResponse(redirect_url)
