# Author: Nina Mislej
# Date created: 5.12.2024

import uvicorn
from fastapi import FastAPI
from .api import users_api

app = FastAPI(
    title="My API",
    docs_url="/docs",             # Swagger UI
    redoc_url="/redoc",           # Redoc UI
    openapi_url="/openapi.json"   # OpenAPI schema URL
)

app.include_router(users_api.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)