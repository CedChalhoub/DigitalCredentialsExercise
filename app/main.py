from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()
app.include_router(credential_status.router)

handler = Mangum(app)
