# Author: Nina Mislej
# Date created: 09.01.2025

# Enable async testing.
import pytest
from unittest.mock import AsyncMock, patch

# Internal app dependencies.
from app.services import sensor_utils, user_utils
from app.schemas import sensor_schemas, user_schemas
from app.helpers import ErrorResponse as Err
from app.helpers import get_collection as gc
from .helpers import get_collection, USERNAME

# NOTE: If the function passed to the patch should mimic an async one use:
# CODE: AsyncMock(return_value=get_collection())

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.sensor_utils.get_collection", get_collection)
async def test_create_sensor(client, cleanup):
    """
    Test creating three sensors for a user.

    Asserts:
        - The sensor API responds with a 200 status code for a temperature sensor.
        - The sensor API responds with a 200 status code for a humidity sensor.
        - The sensor API responds with a 200 status code for a door sensor.
        - The sensor cannot be created if name already exists, returns 409 status code.
    """

    # Test successful request for humidity sensor.
    username = await user_utils.create_user(user_schemas.UserCreate(username=USERNAME))
    assert not isinstance(username, Err)
    cleanup.append(username)
    sensor_create = sensor_schemas.HumiditySensorCreate(name="MerilecVlage").model_dump()
    response = await client.post(url=f"/sensors/{username}/create-humidity-sensor", json=sensor_create)
    assert response.status_code == 200

    # Test successful request for temperature sensor.
    sensor_create = sensor_schemas.TemperatureSensorCreate(name="Termometer").model_dump()
    response = await client.post(url=f"/sensors/{username}/create-temperature-sensor", json=sensor_create)
    assert response.status_code == 200

    # Test successful request for door sensor.
    sensor_create = sensor_schemas.DoorSensorCreate(name="VhodnaVrata").model_dump()
    response = await client.post(url=f"/sensors/{username}/create-door-sensor", json=sensor_create)
    assert response.status_code == 200

    # Test duplicated name unsuccessful request.
    response = await client.post(url=f"/sensors/{username}/create-door-sensor", json=sensor_create)
    assert response.status_code == 409

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.sensor_utils.get_collection", get_collection)
async def test_get_sensor(client, cleanup):
    """
    Test retrieving a sensor by its name.

    Asserts:
        - The sensor API responds with a 200 status code for a temperature sensor.
        - The sensor API responds with a 200 status code for a humidity sensor.
        - The sensor API responds with a 200 status code for a door sensor.
    """

    # Test successful request for a humidity sensor.
    username = await user_utils.create_user(user_schemas.UserCreate(username=USERNAME))
    assert not isinstance(username, Err)
    cleanup.append(username)
    sensor = sensor_schemas.HumiditySensorCreate(name="MerilecVlage")
    sensor_name = await sensor_utils.create_humidity_sensor(username, sensor)
    assert not isinstance(sensor_name, Err)
    response = await client.get(url=f"/sensors/{username}/{sensor_name}")
    assert response.status_code == 200

    # Test successful request for a temperature sensor.
    sensor = sensor_schemas.TemperatureSensorCreate(name="Termoemeter")
    sensor_name = await sensor_utils.create_temperature_sensor(username, sensor)
    assert not isinstance(sensor_name, Err)
    response = await client.get(url=f"/sensors/{username}/{sensor_name}")
    assert response.status_code == 200

    # Test successful request for the door sensor.
    sensor = sensor_schemas.DoorSensorCreate(name="VhodnaVrata")
    sensor_name = await sensor_utils.create_door_sensor(username, sensor)
    assert not isinstance(sensor_name, Err)
    response = await client.get(url=f"/sensors/{username}/{sensor_name}")
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.sensor_utils.get_collection", get_collection)
async def test_delete_sensor(client, cleanup):
    """
    Test deleting a sensor by its name.

    Asserts:
        - The sensor API responds with a 200 status code.
    """

    # Test successful request.
    username = await user_utils.create_user(user_schemas.UserCreate(username=USERNAME))
    assert not isinstance(username, Err)
    cleanup.append(username)
    sensor = sensor_schemas.DoorSensorCreate(name="VhodnaVrata")
    sensor_name = await sensor_utils.create_door_sensor(username, sensor)
    assert not isinstance(sensor_name, Err)
    response = await client.delete(url=f"/sensors/{username}/{sensor_name}")
    assert response.status_code == 200

@pytest.mark.anyio
@patch("app.services.user_utils.get_collection", get_collection)
@patch("app.services.sensor_utils.get_collection", get_collection)
async def test_update_sensor_name(client, cleanup):
    """
    Test updating a sensor's name.

    Asserts:
        - The sensor name update API responds with a 200 status code.
        - The sensor cannot be updated if name already exists, returns 409 status code.
    """

    # Test successful request.
    username = await user_utils.create_user(user_schemas.UserCreate(username=USERNAME))
    assert not isinstance(username, Err)
    cleanup.append(username)
    sensor = sensor_schemas.DoorSensorCreate(name="VhodnaVrata")
    sensor_name = await sensor_utils.create_door_sensor(username, sensor)
    assert not isinstance(sensor_name, Err)
    new_name = "BalkonskaVrata"
    response = await client.put(url=f"/sensors/{username}/{sensor_name}/update-name",
                                params={"new_name": new_name})
    assert response.status_code == 200

    # Test duplicated name unsuccessful request.
    sensor = sensor_schemas.DoorSensorCreate(name="ZadnjaVrata")
    duplicated_name = await sensor_utils.create_door_sensor(username, sensor)
    assert not isinstance(new_name, Err)
    response = await client.put(url=f"/sensors/{username}/{new_name}/update-name",
                                params={"new_name": duplicated_name})
    assert response.status_code == 409