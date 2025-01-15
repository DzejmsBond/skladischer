"""
The `rabbitmq` module provides utility functions for sending and recieving messages from the RabbitMQ API.
It pre-processes the data before sending it to the channel and post-processes it afterward.
"""

from .sensor_data_exchange import (
    send_to_channel,
    receive_from_channel)