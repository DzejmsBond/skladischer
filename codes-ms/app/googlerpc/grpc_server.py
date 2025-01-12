# Author: Nina Mislej
# Date created: 5.12.2024

# Internal dependencies.
from ..schemas import code_schemas as schema
from ..helpers.error import ErrorResponse as Err
from ..services import code_utils as utils

# GRPC Logic.
import asyncio
from concurrent import futures
from proto import code_ms_pb2_grpc as pb_grpc
from proto import code_ms_pb2 as pb
from proto.config import CREATE_CODE_PORT
import grpc

class CodeService(pb_grpc.CodeServiceServicer):
    async def CreateCode(self, request, context):
        code_info = schema.CodeCreate(code_id=request.item_code)
        result = await utils.create_code(code_info)
        if isinstance(result, Err):
            context.set_code(400)
            context.set_details(result.message)
        return pb.CodeResponse(image_base64=result)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_CodeServiceServicer_to_server(CodeService(), server)
    server.add_insecure_port(f"[::]:{CREATE_CODE_PORT}")
    await server.start()
    await server.wait_for_termination()