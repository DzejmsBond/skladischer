# Author: Nina Mislej
# Date created: 5.12.2024

# Internal dependencies.
from ..schemas import user_schemas as schema
from ..helpers.error import ErrorResponse as Err
from ..services import user_utils as utils

# GRPC Logic.
import asyncio
from concurrent import futures
from proto import sensor_ms_pb2_grpc as pb_grpc
from proto import sensor_ms_pb2 as pb
from proto.config import PORT_SENSOR
import grpc

class SensorService(pb_grpc.SensorServiceServicer):
    """
    Handles the GRPC request for creating a user.

    Args:
        request (pb.UserRequest): The GRPC request object containing the username.
        context: The GRPC context for the request. Used for error handling.

    Returns:
        pb.UserResponse: A gRPC response containing the username.
    """

    async def CreateUser(self, request, context):
        """
        Handles the gRPC request to create a new user.

        Args:
            request: The gRPC request containing the `username` to create.
            context: The gRPC context for managing request metadata and status.

        Returns:
            pb.UserResponse: A response containing the created username.
                             Returns an empty response with a 400 status if an error occurs.
        """
        user_info = schema.UserCreate(username=request.username)
        result = await utils.create_user(user_info)
        if isinstance(result, Err):
            context.set_code(400)
            context.set_details(result.message)
            return pb.UserResponse()
        return pb.UserResponse(username=result)

    async def DeleteUser(self, request, context):
        """
        Handles the gRPC request to delete an existing user.

        Args:
            request: The gRPC request containing the `username` to delete.
            context: The gRPC context for managing request metadata and status.

        Returns:
            pb.UserResponse: A response containing the deleted username.
                             Returns an empty response with a 400 status if an error occurs.
        """

        result = await utils.delete_user(request.username)
        if isinstance(result, Err):
            context.set_code(400)
            context.set_details(result.message)
            return pb.UserResponse()
        return pb.UserResponse(username=result)

async def serve():
    """
    Starts the GRPC server to handle sensor microservice internal requests.

    The server listens for incoming requests on the configured ports
    and registers the `UserService` handler for GRPC calls.
    """

    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_SensorServiceServicer_to_server(SensorService(), server)
    server.add_insecure_port(f"[::]:{PORT_SENSOR}")
    await server.start()
    await server.wait_for_termination()