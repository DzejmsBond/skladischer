# Author: Nina Mislej
# Date created: 5.12.2024

# Internal dependencies.
from ..config import STORAGE_MS_HOST

# GRPC Logic.
import asyncio
from proto import storage_ms_pb2_grpc as pb_grpc
from proto import storage_ms_pb2 as pb
from proto.config import CREATE_USER_PORT, DELETE_USER_PORT
import grpc

async def create_user(username : str) -> str:
    """
    Sends a GRPC request to the UserService to create a user with the given username.

    Args:
        username (str): The unique username of the user created.

    Returns:
        str: The username of the created user.
    """

    async with grpc.aio.insecure_channel(f"{STORAGE_MS_HOST}:{CREATE_USER_PORT}") as channel:
        stub = pb_grpc.StorageServiceStub(channel)
        response = await stub.CreateUser(pb.UserRequest(username=username))
    return response.username

async def delete_user(username : str) -> str:
    """
    Sends a GRPC request to the UserService to delete a user with the given username.

    Args:
        username (str): The unique username of the user deleted.

    Returns:
        str: The username of the deleted user.
    """

    async with grpc.aio.insecure_channel(f"{STORAGE_MS_HOST}:{DELETE_USER_PORT}") as channel:
        stub = pb_grpc.StorageServiceStub(channel)
        response = await stub.DeleteUser(pb.UserRequest(username=username))
    return response.username
