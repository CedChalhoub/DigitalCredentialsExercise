from mangum import Mangum
from fastapi import FastAPI

from app.interfaces.rest.dto.assembler_registry import AssemblerRegistry

from app.interfaces.rest.exceptions.middleware import setup_exception_handlers
from app.interfaces.rest.routes.credential_router import CredentialRouter


def create_app() -> FastAPI:
    app = FastAPI()
    setup_exception_handlers(app)
    app.include_router(CredentialRouter(AssemblerRegistry()).router)
    return app

app = create_app()
handler = Mangum(app, lifespan="off")