# Author: Nina Mislej
# Date created: 5.12.2024

# REST and GRPC dependencies.
import asyncio
import uvicorn
from fastapi import FastAPI

# Internal dependencies.
from .api import (
    credentials_api,
    health_check_api)

# Logging default library.
from .logger_setup import get_logger
logger = get_logger("admin-ms.main")

app = FastAPI(
    title="Admin Managment Microservice",
    docs_url="/credentials/docs-api",         # Swagger UI
    redoc_url="/credentials/redoc",           # Redoc UI
    openapi_url="/credentials/openapi.json"   # OpenAPI schema URL
)

# Include all routers and mounts.
app.include_router(credentials_api.router)
app.include_router(health_check_api.router)

async def start_api():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8001)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    tasks = [start_api()]
    return await asyncio.gather(*tasks)

# Run the application with asyncio.
if __name__ == "__main__":
    logger.info("Starting Admin Microservice.")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())