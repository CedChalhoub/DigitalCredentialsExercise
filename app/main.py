from fastapi import FastAPI
from mangum import Mangum

from app.api.routes import credential_resource

app = FastAPI()
app.include_router(credential_resource.router)

handler = Mangum(app)
