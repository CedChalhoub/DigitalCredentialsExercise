from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.exceptions.handlers import ExceptionHandlerRegistry


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        api_exception = ExceptionHandlerRegistry.get_handler(exc)
        return JSONResponse(
            status_code=api_exception.status_code,
            content={"detail": api_exception.detail}
        )