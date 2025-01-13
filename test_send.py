# Author: Nina Mislej
# Date created: 5.12.2024

import pika
import json
from fastapi import FastAPI, HTTPException

app = FastAPI()

# RabbitMQ connection setup
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange="sensor-data-exchange", exchange_type="topic")

channel.basic_publish(
    exchange="sensor-data-exchange",
    routing_key="ananovak",
    body="Hello World!"
)
connection.close()