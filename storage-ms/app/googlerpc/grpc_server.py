# Author: Nina Mislej
# Date created: 5.12.2024

# Internal dependencies.
from ..schemas import user_schemas as schema
from ..helpers.error import ErrorResponse as Err
from ..services import user_utils as utils

# GRPC Logic.
import asyncio
from concurrent import futures
from proto import storage_ms_pb2_grpc as pb_grpc
from proto import storage_ms_pb2 as pb
from proto.config import CREATE_CODE_PORT, DELETE_USER_PORT
import grpc

class StorageService(pb_grpc.StorageServiceServicer):
    """
    Handles the GRPC request for creating a code.

    Args:
        request (pb.CodeRequest): The GRPC request object containing the item code.
        context: The GRPC context for the request. Used for error handling.

    Returns:
        pb.CodeResponse: A gRPC response containing the generated code as a Base64 string.
    """

    async def CreateUser(self, request, context):
        user_info = schema.UserCreate(code_id=request.item_code)
        result = await utils.create_code(code_info)
        if isinstance(result, Err):
            context.set_code(400)
            context.set_details(result.message)
        return pb.CodeResponse(image_base64=result)

    async def DeleteUser(self, request, context):
        user_info = schema.CodeCreate(code_id=request.item_code)
        result = await utils.create_code(code_info)
        if isinstance(result, Err):
            context.set_code(400)
            context.set_details(result.message)
        return pb.CodeResponse(image_base64=result)

async def serve():
    """
    Starts the GRPC server to handle code microservice internal requests.

    The server listens for incoming requests on the configured port
    and registers the `CodeService` handler for GRPC calls.
    """

    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_StorageServiceServicer_to_server(StorageService(), server)
    server.add_insecure_port(f"[::]:{CREATE_CODE_PORT}")
    server.add_insecure_port(f"[::]:{DELETE_USER_PORT}")
    await server.start()
    await server.wait_for_termination()