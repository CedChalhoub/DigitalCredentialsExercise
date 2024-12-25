from mangum import Mangum
from fastapi import FastAPI

from app.api.dto.AssemblerRegistry import AssemblerRegistry

from app.api.dto.PassportAssembler import PassportAssembler
from app.api.dto.DriversLicenseAssembler import DriversLicenseAssembler
from app.api.routes.CredentialRouter import CredentialRouter


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(CredentialRouter(AssemblerRegistry()).router)
    return app

app = create_app()
handler = Mangum(app, lifespan="off")