"""
The `googlerpc` module provides GRPC integration for communication between microservices.
"""

from .grpc_client import (
    create_sensor_user,
    create_storage_user,
    delete_sensor_user,
    delete_storage_user)
