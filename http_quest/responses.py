import typing

from starlette.responses import JSONResponse, PlainTextResponse


class PasswordResponse(JSONResponse):
    def __init__(
        self,
        password: str,
        key: str = "password",
        *args: typing.Any,
        **kwargs: typing.Any
    ) -> None:
        super().__init__({key: password}, *args, **kwargs)


class FinishResponse(PlainTextResponse):
    def __init__(self) -> None:
        super().__init__(
            "You have completed the very last level of HTTP quest. Congratulations!\n\n"
            "Please share you're feedback and ideas for new levels on Github: "
            "https://github.com/2tunnels/http-quest\n\n"
            "Thank you for your time!"
        )
