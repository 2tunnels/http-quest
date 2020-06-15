from starlette.requests import Request
from starlette.responses import PlainTextResponse

from . import passwords, secrets


async def home(_request: Request) -> PlainTextResponse:
    return PlainTextResponse(passwords.PLAIN)


async def robots(_request: Request) -> PlainTextResponse:
    return PlainTextResponse(f"User-agent: *\nDisallow:\n\n# {secrets.ROBOTS}\n")
