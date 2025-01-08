# Author: Nina Mislej
# Date created: 08.01.2025

import uvicorn
from fastapi import FastAPI
from .api import code_api

app = FastAPI(
    title="Code Generation Microservice",
    docs_url="/docs",             # Swagger UI
    redoc_url="/redoc",           # Redoc UI
    openapi_url="/openapi.json"   # OpenAPI schema URL
)

app.include_router(code_api.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)