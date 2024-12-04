from fastapi import FastAPI

from .admin import uporabniki
from .user import skladisca

app = FastAPI()

app.include_router(uporabniki.router)
app.include_router(skladisca.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger World"}