.. Skladischer documentation master file.

Skladischer: Credentials Manager
================================

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

The **Credentials Management Service** provides a secure and robust solution for managing user credentials, ensuring safe password handling and efficient validation.

Core Features
-------------

- **Password Hashing**
  Securely hash passwords before storing them in the database using strong algorithms like `bcrypt`.

- **Validation**
  Verify credentials without ever exposing plaintext passwords, ensuring user data remains secure.

- **CRUD Operations**
  Support for creating, validating, updating, and deleting user credentials through a consistent API.

- **Error Handling**
  Return standardized error messages for invalid requests or authentication failures.

API Endpoints
-------------

.. list-table::
   :header-rows: 1

   * - Endpoint
     - Method
     - Description
   * - :func:`~app.api.create_credentials`
     - POST
     - Create a new user with hashed credentials.
   * - :func:`~app.api.validate_credentials`
     - GET
     - Validate user credentials and return a success response.
   * - :func:`~app.api.delete_credentials`
     - DELETE
     - Remove a user from the system.
   * - :func:`~app.api.update_password`
     - PUT
     - Update a user's password securely.

Technologies Used
-----------------

- **FastAPI**: For building and managing the API endpoints.
- **Pydantic**: For input validation and schema generation.
- **MongoDB**: For storing user credentials and metadata.
- **bcrypt**: For secure password hashing.

Getting Started
---------------

1. Clone the repository::

       git clone https://github.com/DzejmsBond/skladischer.git

2. Install dependencies::

       pip install -r requirements.txt

3. Start the service::

       uvicorn app.main:app --reload

Testing functions that can be used are documented in the :doc:`tests-module`.

