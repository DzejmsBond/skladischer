"""
The `api` module provides implementation of enpoints for the HTTP requests.
"""

from .credentials_api import (
    create_credentials,
    validate_credentials,
    delete_credentials,
    update_password)