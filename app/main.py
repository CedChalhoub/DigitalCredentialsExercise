from fastapi import FastAPI
from mangum import Mangum

from app.api.routes import CredentialRouter

app = FastAPI()
app.include_router(CredentialRouter.router)

handler = Mangum(app)
