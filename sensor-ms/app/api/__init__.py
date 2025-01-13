"""
The `api` module provides implementation of enpoints for the HTTP requests.
"""

from .sensor_api import (
    create_credentials,
    validate_credentials,
    delete_credentials,
    update_password)