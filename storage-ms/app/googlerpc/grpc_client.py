# Author: Nina Mislej
# Date created: 5.12.2024

# Internal dependencies.
from ..config import CODES_MS_HOST

# GRPC Logic.
import asyncio
from proto import code_ms_pb2_grpc as pb_grpc
from proto import code_ms_pb2 as pb
from proto.config import CREATE_CODE_PORT
import grpc

async def create_code(item_code : str) -> None:
    async with grpc.aio.insecure_channel(f"{CODES_MS_HOST}:{CREATE_CODE_PORT}") as channel:
        stub = pb_grpc.CodeServiceStub(channel)
        response = await stub.CreateCode(pb.CodeRequest(item_code=item_code))
    return response.image_base64
