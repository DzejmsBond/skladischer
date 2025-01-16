# Author: Nina Mislej
# Date created: 5.12.2024

# Internal dependencies.
from ..schemas import code_schemas as schema
from ..helpers.error import ErrorResponse as Err
from ..services import code_utils as utils

# GRPC Logic.
import asyncio
from concurrent import futures
from skladischer_proto import code_ms_pb2_grpc as pb_grpc
from skladischer_proto import code_ms_pb2 as pb
from skladischer_proto.config import PORT_CODE
import grpc

class CodeService(pb_grpc.CodeServiceServicer):
    """
    Handles the GRPC request for creating a code.

    Args:
        request (pb.CodeRequest): The GRPC request object containing the item code.
        context: The GRPC context for the request. Used for error handling.

    Returns:
        pb.CodeResponse: A gRPC response containing the generated code as a Base64 string.
    """

    async def CreateCode(self, request, context):
        """
        Handles the gRPC request to create a QR code for a given item.

        Args:
            request: The gRPC request containing the `item_code` to generate the QR code for.
            context: The gRPC context for managing request metadata and status.

        Returns:
            pb.CodeResponse: A response containing the generated QR code as a Base64 string.
                             Returns an empty response with a 400 status if an error occurs.
        """

        code_info = schema.CodeCreate(code_id=request.item_code)
        result = await utils.create_code(code_info)
        if isinstance(result, Err):
            context.set_code(400)
            context.set_details(result.message)
            return pb.CodeResponse()
        return pb.CodeResponse(image_base64=result)

async def serve():
    """
    Starts the GRPC server to handle code microservice internal requests.

    The server listens for incoming requests on the configured port
    and registers the `CodeService` handler for GRPC calls.
    """

    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_CodeServiceServicer_to_server(CodeService(), server)
    server.add_insecure_port(f"[::]:{PORT_CODE}")
    await server.start()
    await server.wait_for_termination()