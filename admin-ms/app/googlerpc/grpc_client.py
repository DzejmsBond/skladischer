# Author: Nina Mislej
# Date created: 5.12.2024

# Logging default library.
import logging

# Internal dependencies.
from ..config import STORAGE_MS_HOST, SENSOR_MS_HOST
from ..helpers.error import ErrorResponse as Err

# GRPC Logic.
import asyncio
from skladischer_proto import storage_ms_pb2_grpc as storage_pb_grpc
from skladischer_proto import storage_ms_pb2 as storage_pb
from skladischer_proto import sensor_ms_pb2_grpc as sensor_pb_grpc
from skladischer_proto import sensor_ms_pb2 as sensor_pb
from skladischer_proto.config import PORT_SENSOR, PORT_STORAGE

import grpc

async def create_storage_user(username : str) -> Err | str:
    """
    Sends a GRPC request to the UserService from Storage server to create a user with the given username.

    Args:
        username (str): The unique username of the user created.

    Returns:
        ErrorResponse | str: The username of the created user or an error response if an error occurred.
    """

    try:
        async with grpc.aio.insecure_channel(f"{STORAGE_MS_HOST}:{PORT_STORAGE}") as channel:
            stub = storage_pb_grpc.StorageServiceStub(channel)
            response = await stub.CreateUser(storage_pb.UserRequest(username=username))
        return response.username

    except Exception as e:
        logging.warning(f"RPC Client failure: {e}")
        return Err(message=f"RPC Error: {e}", code=400)

async def create_sensor_user(username : str) -> Err | str:
    """
    Sends a GRPC request to the UserService from Sensor server to create a user with the given username.

    Args:
        username (str): The unique username of the user created.

    Returns:
        ErrorResponse | str: The username of the created user or an error response if an error occurred.
    """
    try:
        async with grpc.aio.insecure_channel(f"{SENSOR_MS_HOST}:{PORT_SENSOR}") as channel:
            stub = sensor_pb_grpc.SensorServiceStub(channel)
            response = await stub.CreateUser(sensor_pb.UserRequest(username=username))
        return response.username

    except Exception as e:
        logging.warning(f"RPC failure: {e}")
        return Err(message=f"RPC Client Error: {e}", code=400)

async def delete_storage_user(username : str) -> Err | str:
    """
    Sends a GRPC request to the UserService from Storage server to delete a user with the given username.

    Args:
        username (str): The unique username of the user deleted.

    Returns:
        ErrorResponse | str: The username of the created user or an error response if an error occurred.
    """
    try:
        async with grpc.aio.insecure_channel(f"{STORAGE_MS_HOST}:{PORT_STORAGE}") as channel:
            stub = storage_pb_grpc.StorageServiceStub(channel)
            response = await stub.DeleteUser(storage_pb.UserRequest(username=username))
        return response.username

    except Exception as e:
        logging.warning(f"RPC failure: {e}")
        return Err(message=f"RPC Client Error: {e}", code=400)

async def delete_sensor_user(username : str) -> Err | str:
    """
    Sends a GRPC request to the UserService from Sensor server to delete a user with the given username.

    Args:
        username (str): The unique username of the user deleted.

    Returns:
        ErrorResponse | str: The username of the created user or an error response if an error occurred.
    """

    try:
        async with grpc.aio.insecure_channel(f"{SENSOR_MS_HOST}:{PORT_SENSOR}") as channel:
            stub = sensor_pb_grpc.SensorServiceStub(channel)
            response = await stub.DeleteUser(sensor_pb.UserRequest(username=username))
        return response.username

    except Exception as e:
        logging.warning(f"RPC failure: {e}")
        return Err(message=f"RPC Client Error: {e}", code=400)
