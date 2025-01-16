# Author: Nina Mislej
# Date created: 5.12.2024

# Internal dependencies.
from ..config import CODES_MS_HOST

# GRPC Logic.
import asyncio
from skladischer_proto import code_ms_pb2_grpc as pb_grpc
from skladischer_proto import code_ms_pb2 as pb
from skladischer_proto.config import PORT_CODE
import grpc

async def create_code(item_code : str) -> str:
    """
    Sends a GRPC request to the CodeService to create a code for a given item.

    Args:
        item_code (str): The unique identifier of the item for which the code is created.

    Returns:
        str: The generated code image in Base64 format.
    """

    async with grpc.aio.insecure_channel(f"{CODES_MS_HOST}:{PORT_CODE}") as channel:
        stub = pb_grpc.CodeServiceStub(channel)
        response = await stub.CreateCode(pb.CodeRequest(item_code=item_code))
    return response.image_base64
