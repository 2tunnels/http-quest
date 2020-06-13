from functools import wraps
from typing import Any, Callable

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_403_FORBIDDEN


def require_password(password: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Response:
            provided_password = request.headers.get("x-password", "")

            if not provided_password:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail="X-Password header is required",
                )

            if provided_password != password:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="X-Password header is wrong"
                )

            response: Response = await func(request, *args, **kwargs)

            return response

        return wrapper

    return decorator
