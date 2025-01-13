# Author: Nina Mislej
# Date created: 5.12.2024

import pika
import json
from fastapi import FastAPI, HTTPException

app = FastAPI()

# RabbitMQ connection setup
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.exchange_declare(exchange="sensor-data-exchange", exchange_type="fanout")
channel.basic_publish(
        exchange="sensor-data-exchange",
        routing_key="",
        body=json.dumps({"detail": "test message"})
    )
connection.close()