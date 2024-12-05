# Author: Nina Mislej
# Date created: 5.12.2024

from fastapi import FastAPI
from .api import usersApi

app = FastAPI()
app.include_router(usersApi.router)

@app.get("/")
async def root():
    return {"message": "ROOT"}