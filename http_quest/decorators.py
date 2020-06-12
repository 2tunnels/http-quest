from functools import wraps

from starlette.endpoints import HTTPEndpoint
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


def require_password(password: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(endpoint: HTTPEndpoint, request: Request, *args, **kwargs):
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

            return await func(endpoint, request, *args, **kwargs)

        return wrapper

    return decorator
