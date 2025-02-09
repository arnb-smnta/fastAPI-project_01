from fastapi import Request, Response
from typing import Callable, Awaitable

def async_handler(request_handler: Callable[..., Awaitable[Response]]):
    async def wrapper(request: Request, *args, **kwargs):
        try:
            return await request_handler(request, *args, **kwargs)
        except Exception as err:
            return Response(content=str(err), status_code=500)
    return wrapper

__all__ = ["async_handler"]  # Explicit export
