from starlette.requests import Request
from starlette.responses import PlainTextResponse

from . import __version__, passwords, secrets, utils


async def home(request: Request) -> PlainTextResponse:
    url = request.url_for("level:plain")

    return PlainTextResponse(
        f"{utils.get_banner()} v{__version__}\n\n"
        "curl your way through dangerous levels!\n\n"
        "Every level is password protected, "
        "so don't forget to pass it using X-Password header.\n"
        "Solve the puzzle and you will get password for the next level!\n\n"
        f"Password for the first level is: {passwords.PLAIN}\n\n"
        f"$ curl -H 'X-Password:{passwords.PLAIN}' {url}\n\n"
        "If you every feel stuck, just try harder.\n\n"
        "GitHub: https://github.com/2tunnels/http-quest\n"
    )


async def robots(_request: Request) -> PlainTextResponse:
    return PlainTextResponse(f"User-agent: *\nDisallow:\n\n# {secrets.ROBOTS}\n")
