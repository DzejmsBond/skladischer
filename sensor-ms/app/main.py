# Author: Nina Mislej
# Date created: 5.12.2024

# REST and GRPC dependencies.
import asyncio
import uvicorn
from fastapi import FastAPI
from .googlerpc.grpc_server import serve

# Internal dependencies.
from .api import (
    sensor_api,
    users_api,
    sensor_data_api,
    health_check_api)

app = FastAPI(
    title="Sensor Managment Microservice",
    docs_url="/sensors/docs-api",             # Swagger UI
    redoc_url="/sensors/redoc",           # Redoc UI
    openapi_url="/sensors/openapi.json"   # OpenAPI schema URL
)

# Logging default library.
from .logger_setup import get_logger
logger = get_logger("sensor-ms.main")

# Include all routers and mounts.
app.include_router(users_api.router)
app.include_router(sensor_data_api.router)
app.include_router(sensor_api.router)
app.include_router(health_check_api.router)

async def start_api():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8003)
    server = uvicorn.Server(config)
    await server.serve()

async def start_grpc():
    await serve()

async def main():
    tasks = [start_api(), start_grpc()]
    return await asyncio.gather(*tasks)

# Run the application with asyncio.
if __name__ == "__main__":
    logger.info("Starting Sensor Microservice.")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())