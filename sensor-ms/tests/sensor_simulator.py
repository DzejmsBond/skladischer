# Author: Nina Mislej
# Date created: 13.01.2025
import httpx
from httpx import Client
import random
from datetime import datetime, timezone
import time

# TODO: This is a hack.
#       Implement token when implementing authorization.
def generate_temperature_data():

    return {
        "username": "testuser",
        "name": "temperaturetest",
        "temperature": round(random.uniform(18, 30), 2),
        "timestamp": str(datetime.now(tz=timezone.utc))
    }

def generate_humidity_data():

    return {
        "username": "testuser",
        "name": "humiditytest",
        "humidity_level": round(random.uniform(30, 70), 2),
        "timestamp": str(datetime.now(tz=timezone.utc))
    }

def generate_door_data():

    return {
        "username": "testuser",
        "name": "doortest",
        "timestamp": str(datetime.now(tz=timezone.utc))
    }

def send_sensor_data(client, url, data):

    response = client.post(url, json=data, timeout=10.0)
    return response

def sensor_simulator():

    # TODO: This probably shouldn't be hardcoded.
    sensor_url = f"http://34.144.195.148/sensors/sensor-data"
    client = httpx.Client(base_url=sensor_url)
    while True:
        try:
            # Generate test data.
            temperature_data = generate_temperature_data()
            humidity_data = generate_humidity_data()
            door_data = generate_door_data()

            # Send temperature simulation.
            response = send_sensor_data(client, sensor_url, temperature_data)
            print(f"{response.status_code}: Sent temperature {temperature_data.get("temperature")} at {temperature_data.get('timestamp')}: {response.text}")

            # Send humidity simulation.
            response = send_sensor_data(client, sensor_url, humidity_data)
            print(f"{response.status_code}: Sent humidity level {humidity_data.get("humidity_level")} at {humidity_data.get('timestamp')}: {response.text}")

            # Send door simulation.
            response = send_sensor_data(client, sensor_url, door_data)
            print(f"{response.status_code}: Sent door opened at {door_data.get('timestamp')}: {response.text}")

            time.sleep(5) # Send sensor reports per some value.

        except httpx.RequestError as e:
            print(f"Error {e}: Data could not be sent. Trying again in 10 seconds.")
            time.sleep(10)  # Retry after a delay of 1 minute for exceptions.
            continue

        except KeyboardInterrupt:
            print("Sensor stopped.")
            break

if __name__ == "__main__":
    sensor_simulator()