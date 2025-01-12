# Author: Nina Mislej
# Date created: 5.12.2024

# REST and GRPC dependencies.
import asyncio
import uvicorn
from fastapi import FastAPI

# Internal dependencies.
from .api import (
    credentials_api)

app = FastAPI(
    title="Admin Managment Microservice",
    docs_url="/docs",             # Swagger UI
    redoc_url="/redoc",           # Redoc UI
    openapi_url="/openapi.json"   # OpenAPI schema URL
)

# Include all routers and mounts.
app.include_router(credentials_api.router)

async def start_api():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    tasks = [start_api()]
    return await asyncio.gather(*tasks)

# Run the application with asyncio.
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())