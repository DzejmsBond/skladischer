# Author: Nina Mislej
# Date created: 5.12.2024

# GRPC Logic.
import asyncio
from proto import code_ms_pb2_grpc as pb_grpc
from proto import code_ms_pb2 as pb
import grpc

async def create_code(item_code : str) -> None:
    async with grpc.aio.insecure_channel("localhost:8010") as channel:
        stub = pb_grpc.CodeServiceStub(channel)
        response = await stub.CreateCode(pb.CodeRequest(item_code=item_code))
    print("Image received: " + response.image_base64)


if __name__ == '__main__':
    result = asyncio.run(create_code("Test"))