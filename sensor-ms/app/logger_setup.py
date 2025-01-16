# Author: Nina Mislej
# Date created: 5.12.2024

# Logging default library.
import logging

# Imports the Cloud Logging client library.
import google.cloud.logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler

def get_logger(logger_name: str):

    # Instantiates a client.
    # Retrieves a Cloud Logging handler based on the environment
    # you're running in and integrates the handler with the
    # Python logging module. By default, this captures all logs
    # at INFO level and higher.
    client = google.cloud.logging.Client()
    client.setup_logging(log_level=logging.DEBUG)

    # Settup logger.
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                                  datefmt='%m-%d %H:%M')

    # Settup logging handlers and formatting.
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    cloud_handler = CloudLoggingHandler(client)
    cloud_handler.setFormatter(formatter)

    # Add logging handlers.
    logger.addHandler(stream_handler)
    logger.addHandler(cloud_handler)
    return logger