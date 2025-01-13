
#!/usr/bin/env python
import pika, sys, os, json

def main():
    def callback(ch, method, properties, body):
        print(f"Data: {body}")

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.exchange_declare(exchange="sensor-data-exchange", exchange_type="topic")

    # If we wish to disgard the queue as soon as the connection is closed use:
    # CODE: Exclusive=True
    result = channel.queue_declare(queue="ananovak", arguments={"x-max-length": 2})
    channel.queue_bind(exchange="sensor-data-exchange", queue="ananovak")
    channel.basic_consume(queue="ananovak", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)