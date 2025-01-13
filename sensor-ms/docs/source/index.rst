.. Skladischer documentation master file.

Skladischer: Sensor Manager
============================

.. toctree::
   :maxdepth: 1
   :caption: Module Documentation:

   services-module
   schemas-module
   helpers-module
   models-module
   api-module
   tests-module

Overview
--------

The **Sensor Microservice** provides a solution for managing sensor data, including processing, and storage. This service is designed to handle data streams from various sensors, offering integration with messaging systems like *RabbitMQ* for event-driven architectures.

Core Features
-------------

- **Sensor Data Ingestion**
  Accept real-time sensor data via an API and publish it to a message broker (e.g., RabbitMQ) for further processing.

- **Data Validation**
  Validate incoming sensor data using robust schemas before further processing.

- **Error Handling**
  - Use standardized error responses for invalid data or failed operations.

API Endpoints
-------------

.. list-table::
   :header-rows: 1

   * - Endpoint
     - Method
     - Description
   * - :func:`~app.api.create_user`
     - POST
     - Register a new user in the system.
   * - :func:`~app.api.get_user`
     - GET
     - Retrieve user details by username.
   * - :func:`~app.api.delete_user`
     - DELETE
     - Remove a user from the system.
   * - :func:`~app.api.delete_sensors`
     - PUT
     - Delete all sensors for a user.
   * - :func:`~app.api.create_temperature_sensor`
     - POST
     - Register a new temperature sensor for a user.
   * - :func:`~app.api.create_humidity_sensor`
     - POST
     - Register a new humidity sensor for a user.
   * - :func:`~app.api.create_door_sensor`
     - POST
     - Register a new door sensor for a user.
   * - :func:`~app.api.get_sensor`
     - GET
     - Retrieve details of a specific sensor by name.
   * - :func:`~app.api.delete_sensor`
     - DELETE
     - Delete a specific sensor by name.
   * - :func:`~app.api.update_sensor_name`
     - PUT
     - Update the name of a specific sensor.

Technologies Used
-----------------

- **FastAPI**: For building scalable and efficient APIs.
- **RabbitMQ**: For distributing sensor data using message queues.
- **Pydantic**: For validating and serializing sensor data.
- **MongoDB**: For storing sensor metadata.

Getting Started
---------------

1. Clone the repository::

       git clone https://github.com/DzejmsBond/skladischer.git

2. Set up the environment::

       pip install -r requirements.txt

3. Run the service::

       uvicorn app.main:app --reload


Testing functions that can be used are documented in the :doc:`tests-module`.