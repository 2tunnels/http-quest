from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse

from . import passwords
from .decorators import require_password
from .utils import reverse


async def home(request: Request) -> PlainTextResponse:
    return PlainTextResponse(passwords.LEVEL_1)


@require_password(passwords.LEVEL_1)
async def level_1(request: Request) -> JSONResponse:
    return JSONResponse({reverse("password"): reverse(passwords.LEVEL_2)})


@require_password(passwords.LEVEL_2)
async def level_2(request: Request) -> JSONResponse:
    return JSONResponse({"password": passwords.LEVEL_3})
