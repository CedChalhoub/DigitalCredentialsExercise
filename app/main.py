from mangum import Mangum
from fastapi import FastAPI

from app.api.dto.assembler_registry import AssemblerRegistry

from app.api.dto.passport_assembler import PassportAssembler
from app.api.dto.drivers_license_assembler import DriversLicenseAssembler
from app.api.exceptions.middleware import setup_exception_handlers
from app.api.routes.credential_router import CredentialRouter


def create_app() -> FastAPI:
    app = FastAPI()
    setup_exception_handlers(app)
    app.include_router(CredentialRouter(AssemblerRegistry()).router)
    return app

app = create_app()
handler = Mangum(app, lifespan="off")