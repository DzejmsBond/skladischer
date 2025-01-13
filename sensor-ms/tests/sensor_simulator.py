# Author: Nina Mislej
# Date created: 13.01.2025
import httpx
from httpx import Client
import random
import time


# TODO: This is a hack.
#       Implement token when implementing authorization.
def generate_sensor_data():

    return {
        "username": "testuser",
        "name": "testsensor",
        "temperature": round(random.uniform(18, 30), 2),
        "timestamp": time.time(),
    }

def send_sensor_data(client, url, data):

    response = client.post(url, json=data, timeout=10.0)
    return response

def sensor_simulator():

    # TODO: This probably shouldn't be hardcoded.
    sensor_url = f"http://localhost:8003/sensors/sensor-data"
    client = httpx.Client(base_url=sensor_url)
    while True:
        try:
            data = generate_sensor_data()
            response = send_sensor_data(client, sensor_url, data)
            print(f"{response.status_code}: Sent sensor data at {data.get('timestamp')}: {response.text}")
            time.sleep(1)
        except httpx.RequestError as e:
            print(f"Error {e}: Data could not be sent. Trying again in 10 seconds.")
            time.sleep(10)  # Retry after a delay for exceptions.
            continue
        except KeyboardInterrupt:
            print("Sensor stopped.")
            break

if __name__ == "__main__":
    sensor_simulator()