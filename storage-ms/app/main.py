# Author: Nina Mislej
# Date created: 5.12.2024

import uvicorn
from fastapi import FastAPI
from .api import users_api, item_api, storage_api, health_check_api

app = FastAPI(
    title="Storage Managment Microservice",
    docs_url="/docs",             # Swagger UI
    redoc_url="/redoc",           # Redoc UI
    openapi_url="/openapi.json"   # OpenAPI schema URL
)

app.include_router(users_api.router)
app.include_router(item_api.router)
app.include_router(storage_api.router)
app.include_router(health_check_api.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)