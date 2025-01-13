"""
The `api` module provides implementation of enpoints for the HTTP requests.
"""

from .sensor_api import (
    create_door_sensor,
    create_humidity_sensor,
    create_temperature_sensor,
    get_sensor,
    delete_sensor,
    update_sensor_name)

from .users_api import (
    create_user,
    delete_user,
    get_user,
    delete_sensors)