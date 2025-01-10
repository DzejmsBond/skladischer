.. Skladischer documentation master file.

Skladischer: Storage Manager
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

The **Storage Microservice** provides a robust solution for managing user-defined storage units, items, and inventory.
This service is designed to handle the creation, retrieval, updating, and deletion of storages and their associated items,
offering seamless integration with a scalable database system.

Core Features
-------------

- **User-Specific Storage Management**
    Create, retrieve, update, and delete storages linked to individual users. Maintain unique storage names per user.

- **Item Management**
  Add, retrieve, update, and remove items within a storage. Enforce item uniqueness using a ``code_id``.

- **Error Handling**
  - Use standardized error responses for operations that fail, such as invalid inputs or database errors.

API Endpoints
-------------

.. list-table::
   :header-rows: 1

   * - Endpoint
     - Method
     - Description
   * - :func:`~app.api.create_user`
     - POST
     - Create a new user.
   * - :func:`~app.api.get_user`
     - POST
     - Retrieve an user by its id.
   * - :func:`~app.api.delete_user`
     - DELETE
     - Delete an user by its id.
   * - :func:`~app.api.update_display_name`
     - PUT
     - Updates users display name.
   * - :func:`~app.api.empty_storages`
     - PUT
     - Delete all storages of user.
   * - :func:`~app.api.create_storage`
     - POST
     - Create a new storage for a user.
   * - :func:`~app.api.get_storage`
     - GET
     - Retrieve a storage by its name.
   * - :func:`~app.api.delete_storage`
     - DELETE
     - Delete a storage by its name.
   * - :func:`~app.api.update_storage_name`
     - PUT
     - Update the name of a storage.
   * - :func:`~app.api.empty_storage`
     - PUT
     - Clear all items in a storage.
   * - :func:`~app.api.create_item`
     - POST
     - Add a new item to a storage.
   * - :func:`~app.api.get_item`
     - GET
     - Retrieve an item by its unique code.
   * - :func:`~app.api.delete_item`
     - DELETE
     - Remove an item by its unique code.
   * - :func:`~app.api.update_item`
     - PUT
     - Update item details in a storage.

Technologies Used
-----------------

- **FastAPI**: For building scalable and easy-to-use APIs.
- **MongoDB**: For storing user, storage, and item data.
- **Pydantic**: For data validation and serialization.

Getting Started
---------------

1. Clone the repository::

       git clone https://github.com/DzejmsBond/skladischer.git

2. Set up the environment::

       pip install -r requirements.txt

3. Run the service::

       uvicorn app.main:app --reload


Testing functions that can be used are documented in the :doc:`tests-module`.