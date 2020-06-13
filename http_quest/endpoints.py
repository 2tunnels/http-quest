from typing import Union

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_406_NOT_ACCEPTABLE,
)

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
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Wrong secret")

    try:
        next_secret = chain_of_secrets[index + 1]
    except IndexError:
        return JSONResponse({"password": passwords.LEVEL_7})

    redirect_url = request.url_for("level_6") + "?secret=" + next_secret

    return RedirectResponse(redirect_url)


@require_password(passwords.LEVEL_7)
async def level_7(request: Request) -> JSONResponse:
    """Return plain password for users with Internet Explorer 6 user agent."""

    user_agent = request.headers.get("user-agent", "").lower()

    if "msie 6.0" not in user_agent:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=(
                "Password for the next level is only available for the bravest! "
                "Internet Explorer 6 users!"
            ),
        )

    return JSONResponse({"password": passwords.LEVEL_8})


@require_password(passwords.LEVEL_8)
async def level_8(request: Request) -> JSONResponse:
    """Return plain password for users who guessed the secret number."""

    provided_number = request.query_params.get("number")

    if not provided_number:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=(
                "Guess the number between 1 and 1000. "
                "Provide you guess with 'number' query parameter."
            ),
        )

    try:
        provided_number = int(provided_number)
    except ValueError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Please provide a number."
        )

    if provided_number < 1 or provided_number > 1000:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"{provided_number} is not between 1 and 1000.",
        )

    if provided_number != 372:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Wrong number.")

    return JSONResponse({"password": passwords.LEVEL_9})


@require_password(passwords.LEVEL_9)
async def level_9(request: Request) -> JSONResponse:
    """Return plain password only for russian Accept-Language header."""

    accept_language = request.headers.get("accept-language", "").lower()

    if "ru" not in accept_language:
        raise HTTPException(
            status_code=HTTP_406_NOT_ACCEPTABLE,
            detail="Я говорю только по русски, товарищ.",
        )

    return JSONResponse({"пароль": passwords.LEVEL_10})
