from fastapi import FastAPI

from .dependencies import *
from .admin import uporabniki
from .user import produkti, skladisca
from .qr_kode import qr_kode

app = FastAPI()

app.include_router(uporabniki.router)
app.include_router(skladisca.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger World"}