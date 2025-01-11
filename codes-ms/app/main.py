# Author: Nina Mislej
# Date created: 08.01.2025

import uvicorn
from fastapi import FastAPI
from .api import code_api, health_check_api
# TODO: dependencies should be managed on a microservice-to-microservice basis.
#       Not every microservice has to import all dependencies from "pip freeze" output.

app = FastAPI(
    title="Code Generation Microservice",
    docs_url="/docs",             # Swagger UI
    redoc_url="/redoc",           # Redoc UI
    openapi_url="/openapi.json"   # OpenAPI schema URL
)

app.include_router(code_api.router)
app.include_router(health_check_api.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)