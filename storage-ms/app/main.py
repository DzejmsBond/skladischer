# Author: Nina Mislej
# Date created: 5.12.2024

# REST and GRPC dependencies.
import asyncio
import uvicorn
from fastapi import FastAPI
from .googlerpc.grpc_server import serve

# GraphQL dependencies.
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from pathlib import Path

# Internal dependencies.
from .graphql import resolvers
from .api import (
    users_api,
    item_api,
    storage_api,
    health_check_api)

app = FastAPI(
    title="Storage Managment Microservice",
    docs_url="/docs",             # Swagger UI
    redoc_url="/redoc",           # Redoc UI
    openapi_url="/openapi.json"   # OpenAPI schema URL
)

# Used by graphQL to create schemas.
path = Path(__file__).resolve().parent / 'graphql' / 'schemas.graphql'
type_defs = load_schema_from_path(path)
schema = make_executable_schema(type_defs, [resolvers.query, resolvers.items])

# Include all routers and mounts.
app.include_router(users_api.router)
app.include_router(item_api.router)
app.include_router(storage_api.router)
app.include_router(health_check_api.router)

# To test the endpoint use:
# CODE: GraphQL(schema, debug=True)
app.mount("/users/", GraphQL(schema))

async def start_api():
    config = uvicorn.Config(app=app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

async def start_grpc():
    await serve()

async def main():
    tasks = [start_api(), start_grpc()]
    return await asyncio.gather(*tasks)

# Run the application with asyncio.
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())