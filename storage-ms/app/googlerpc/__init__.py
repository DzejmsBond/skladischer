"""
The `googlerpc` module provides GRPC integration for communication between microservices.
"""

from .grpc_client import (
    create_code)

from .grpc_server import (
    StorageService,
    serve)