"""
The `services` module provides utility functions for managing sensors of users.
It serves as communication between models and the database.
"""

from .sensor_utils import (
    update_sensor_name,
    create_humidity_sensor,
    create_temperature_sensor,
    create_door_sensor,
    delete_sensor,
    get_sensor)

from .user_utils import (
    create_user,
    get_user,
    delete_user,
    delete_sensors)
