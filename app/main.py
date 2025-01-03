from mangum import Mangum
from fastapi import FastAPI

from app.rest.assemblers.assembler_registry import AssemblerRegistry
from app.rest.assemblers.drivers_license_assembler import DriversLicenseAssembler
from app.rest.assemblers.passport_assembler import PassportAssembler
from app.rest.exceptions.credential_middleware import setup_exception_handlers
from app.rest.routes.api_key_router import ApiKeyRouter
from app.rest.routes.credential_router import CredentialRouter



app = FastAPI(
    title="Credential Status API",
    description="API for managing credentials",
    version="0.1.0"
)

setup_exception_handlers(app)
assembler_registry = AssemblerRegistry()
credential_router = CredentialRouter(assembler_registry)
api_key_router = ApiKeyRouter()
app.include_router(api_key_router.router)
app.include_router(credential_router.router)

handler = Mangum(app, lifespan="off")

@app.get("/")
async def heartbeat():
    return {"status": "ok"}