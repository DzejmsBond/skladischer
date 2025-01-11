# Author: Nina Mislej
# Date created: 08.01.2025

import asyncio
import uvicorn
from fastapi import FastAPI
from .api import code_api, health_check_api
from .googlerpc.grpc_server import serve
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

async def start_api():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8002)
    server = uvicorn.Server(config)
    await server.serve()

async def start_grpc():
    await serve()

async def main():
    tasks = [start_api(), start_grpc()]
    return await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
