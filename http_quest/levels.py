import typing
from json import JSONDecodeError

from marshmallow import ValidationError
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from . import passwords, secrets
from .decorators import require_password
from .responses import PasswordResponse
from .schemas import Level8Schema, SecretSchema
from .utils import add_query_params, base64_encode, get_masked_password


@require_password(passwords.PLAIN)
async def plain(_request: Request) -> JSONResponse:
    """Return plain password."""

    return PasswordResponse(passwords.REVERSE)


@require_password(passwords.REVERSE)
async def reverse(_request: Request) -> JSONResponse:
    """Return reversed password."""

    return PasswordResponse(passwords.BASE64[::-1], key="password"[::-1])


@require_password(passwords.BASE64)
async def base64(_request: Request) -> JSONResponse:
    """Return base64 encoded password."""

    return PasswordResponse(base64_encode(passwords.HEADERS))


@require_password(passwords.HEADERS)
async def header(_request: Request) -> JSONResponse:
    """Return fake password in body and real one in header."""

    return PasswordResponse("qwerty", headers={"X-Real-Password": passwords.DELETE})


@require_password(passwords.DELETE)
async def delete(_request: Request) -> JSONResponse:
    """Return plain password. Endpoint will be available only for DELETE method."""

    return PasswordResponse(passwords.REDIRECT)


@require_password(passwords.REDIRECT)
async def redirect(request: Request) -> typing.Union[RedirectResponse, JSONResponse]:
    """Return plain password if user follows redirect chain."""

    url = request.url_for("level:redirect")
    secret = request.query_params.get("secret", "")

    # If secret is not given, use first secret in redirect chain
    if not secret:
        return RedirectResponse(add_query_params(url, secret=secrets.REDIRECT[0]))

    try:
        index = secrets.REDIRECT.index(secret)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Secret is wrong."
        )

    try:
        next_secret = secrets.REDIRECT[index + 1]
    except IndexError:
        return PasswordResponse(passwords.USER_AGENT)

    return RedirectResponse(add_query_params(url, secret=next_secret))


@require_password(passwords.USER_AGENT)
async def user_agent(request: Request) -> JSONResponse:
    """Return plain password for users with Internet Explorer 6 user agent."""

    user_agent_header = request.headers.get("user-agent", "").lower()

    if "msie 6.0" not in user_agent_header:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Password for the next level is only available for the bravest! "
                "Internet Explorer 6 users!"
            ),
        )

    return PasswordResponse(passwords.NUMBER)


@require_password(passwords.NUMBER)
async def guess_number(request: Request) -> JSONResponse:
    """Return plain password for users who guessed the secret number."""

    try:
        body = await request.json()
    except JSONDecodeError:
        body = {}

    schema = Level8Schema()

    try:
        data = schema.load(body)
    except ValidationError as exc:
        return JSONResponse(
            {"errors": exc.messages}, status_code=status.HTTP_400_BAD_REQUEST
        )

    if data["number"] != 372:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Number is wrong."
        )

    return JSONResponse({"password": passwords.ACCEPT_LANGUAGE})


@require_password(passwords.ACCEPT_LANGUAGE)
async def accept_language(request: Request) -> JSONResponse:
    """Return plain password only for russian Accept-Language header."""

    accept_language_header = request.headers.get("accept-language", "").lower()

    if "ru" not in accept_language_header:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Я говорю только по русски, товарищ.",
        )

    return PasswordResponse(passwords.MASK, key="пароль")


@require_password(passwords.MASK)
async def mask(request: Request) -> JSONResponse:
    """Return masked password, based on correctness of given secret."""

    try:
        body = await request.json()
    except JSONDecodeError:
        body = {}

    schema = SecretSchema()

    try:
        data = schema.load(body)
    except ValidationError as exc:
        return JSONResponse(
            {"errors": exc.messages}, status_code=status.HTTP_400_BAD_REQUEST
        )

    return PasswordResponse(
        get_masked_password(passwords.ROBOTS, secrets.MASK, data["secret"])
    )


@require_password(passwords.ROBOTS)
async def robots(request: Request) -> JSONResponse:
    try:
        body = await request.json()
    except JSONDecodeError:
        body = {}

    schema = SecretSchema()

    try:
        data = schema.load(body)
    except ValidationError as exc:
        return JSONResponse(
            {"errors": exc.messages}, status_code=status.HTTP_400_BAD_REQUEST
        )

    if data["secret"] != secrets.ROBOTS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Secret is wrong, human."
        )

    return PasswordResponse(passwords.LEVEL_12)
