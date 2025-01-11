# Author: Nina Mislej
# Date created: 5.12.2024


# Internal dependencies.
from ..schemas import code_schemas as schema
from ..helpers.error import ErrorResponse as Err
from ..services import code_utils as utils

# GRPC Logic.
import asyncio
from concurrent import futures
from proto import code_ms_pb2_grpc
from proto import code_ms_pb2
import grpc

class CodeService(code_ms_pb2_grpc.CodeServiceServicer):
    async def CreateCode(self, request, context):
        code_info = schema.CodeCreate(code_id=request.item_code)
        result = await utils.create_code(code_info)
        if isinstance(result, Err):
            context.set_code(400)
            context.set_details(result.message)
        return code_ms_pb2.CodeResponse(image_base64=result)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    code_ms_pb2_grpc.add_CodeServiceServicer_to_server(CodeService(), server)
    server.add_insecure_port('[::]:8010')
    await server.start()
    await server.wait_for_termination()