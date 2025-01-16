# Author: Nina Mislej
# Date created: 5.12.2024

# RabbitMQ dependencies.
import pika
import json

# Internal dependencies.
from ..config import RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_USER
from ..helpers.error import ErrorResponse as Err
from ..services import sensor_data_utils, user_utils
from ..schemas.user_schemas import GetSensorData

# TODO: This is not the best usecase because all users sensors
#       output on the same queue so if one sensor is publishing information per second and the
#       other per hour the second sensor would get lost.

EXCHANGE_NAME = "sensor-data-exchange"
EXCHANGE_TYPE = "topic"
QUEUE_LENGTH = 100

async def send_to_channel(data: dict) -> str | Err:
    """
    Sends sensor data to the RabbitMQ exchange for processing. The username is parsed from the raw data dictionary.

    Args:
        data (dict): The raw sensor data to send.

    Returns:
        str | ErrorResponse: Confirmation message if successful, or an error if failure occurs while sending data.
    """

    try:
        if "username" not in data:
            return Err(message="No username provided in sensor data.")

        username = data["username"]
        processed_data = await sensor_data_utils.pre_process_data(data)
        if isinstance(processed_data, Err):
            return processed_data
        if not processed_data:
            return Err(message="Sensor processed.")

        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST,
                                                                       credentials=credentials))
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE)

        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=username,
            body=json.dumps(data)
        )
        connection.close()
        return "Sensor processed."

    except Exception as e:
        return Err(message=f"Error while sending data to channel: {e}")

async def receive_from_channel(username: str) -> GetSensorData | Err:
    """
    Retrieves sensor data for a specific user from RabbitMQ and processes it.

    Args:
        username (str): The username for which sensor data is retrieved.

    Returns:
        schema.GetSensorData: The processed sensor data for the user or an error response if an error occurs while receiving or processing data.
    """

    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST,
                                                                       credentials=credentials))
        channel = connection.channel()
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type=EXCHANGE_TYPE)

        queue_info = channel.queue_declare(queue=username, arguments={"x-max-length": QUEUE_LENGTH})
        channel.queue_bind(exchange="sensor-data-exchange", queue=username)

        message_count = 0
        messages_queued = queue_info.method.message_count
        queue = []
        def limited_callback(ch, method, properties, body):
            nonlocal message_count
            nonlocal queue
            data = json.loads(body)
            queue.append(data)
            message_count += 1

            # Stop consuming after reaching max_messages.
            if message_count >= messages_queued:
                channel.stop_consuming()

        if queue_info.method.message_count == 0:
            return Err(message="No sensor data recieved in the channel.")

        channel.basic_consume(queue=username, on_message_callback=limited_callback, auto_ack=True)
        channel.start_consuming()
        connection.close()

        processed_queue = await sensor_data_utils.process_queue(username, queue)
        if isinstance(processed_queue, Err):
            return processed_queue

        door_sensors = await user_utils.get_all_door_sensors(username)
        if isinstance(door_sensors, Err):
            return door_sensors

        for door_sensor in door_sensors:
            if "name" in door_sensor:
                processed_queue.sensors[door_sensor["name"]] = door_sensor
        return processed_queue

    except Exception as e:
        return Err(message=f"Error while recieving data from channel: {e}")