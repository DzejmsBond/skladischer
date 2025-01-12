"""
The `services` module provides utility functions for managing items in storage.
It serves as communication between models and the database.
"""

from .credentials_utils import (
    create_credentials,
    delete_credentials,
    validate_credentials,
    update_password)
