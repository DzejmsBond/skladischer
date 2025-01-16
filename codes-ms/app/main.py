# Author: Nina Mislej
# Date created: 08.01.2025

# REST and GRPC dependencies.
import asyncio
import uvicorn
from fastapi import FastAPI
from .googlerpc.grpc_server import serve

# Internal dependencies.
from .api import code_api, health_check_api

# TODO: dependencies should be managed on a microservice-to-microservice basis.
#       Not every microservice has to import all dependencies from "pip freeze" output.

app = FastAPI(
    title="Code Generation Microservice",
    docs_url="/codes/docs-api",             # Swagger UI
    redoc_url="/codes/redoc",           # Redoc UI
    openapi_url="/codes/openapi.json"   # OpenAPI schema URL
)

# Logging default library.
from .logger_setup import get_logger
logger = get_logger("codes-ms.main")

# Include all routers and mounts.
app.include_router(code_api.router)
app.include_router(health_check_api.router)

async def start_api():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8002)
    server = uvicorn.Server(config)
    await server.serve()

async def start_grpc():
    await serve()

async def main():
    tasks = [start_api(), start_grpc()]
    return await asyncio.gather(*tasks)

# Run the application with asyncio.
if __name__ == "__main__":
    logger.info("Starting Item Code Microservice.")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
