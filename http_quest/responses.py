import typing

from starlette.responses import JSONResponse


class PasswordResponse(JSONResponse):
    def __init__(
        self,
        password: str,
        key: str = "password",
        *args: typing.Any,
        **kwargs: typing.Any
    ) -> None:
        super().__init__({key: password}, *args, **kwargs)
