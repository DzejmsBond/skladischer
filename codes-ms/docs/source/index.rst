.. Skladischer documentation master file.

Skladischer: Item Code Manager
==============================

.. toctree::
   :maxdepth: 1
   :caption: Module Documentation:

   services-module
   schemas-module
   helpers-module
   api-module

Overview
--------

The **QR Code Microservice** is a utility service for generating and managing QR codes.
It integrates with the **Storage Microservice** to provide quick access to storage units and items through QR codes.

Core Features
-------------

- **QR Code Generation**
  Generate QR codes for storages and items. Codes are encoded and saved to items. Support for barcodes and custom hashes as well.

- **Integration with Storage Microservice**
  Automatically link generated QR codes to storages or items. Enable fast retrieval and updates via QR scans.

- **Customizable QR Codes**
  Include user-defined metadata or links in the generated QR codes.

- **Error Handling**
  Handle invalid requests with standardized error responses.

API Endpoints
-------------

.. list-table::
   :header-rows: 1

   * - Endpoint
     - Method
     - Description
   * - :func:`~app.api.create_code`
     - POST
     - Generate a QR code for a specific item.

Technologies Used
-----------------

- **FastAPI**: For building and managing the API endpoints.
- **Pydantic**: For data validation and serialization.
- **MongoDB**: For storing metadata and QR code details.
- **QR code generator API**: Reliable and simple outsourced code generation.

Getting Started
---------------

1. Clone the repository::

       git clone https://github.com/DzejmsBond/skladischer.git

2. Install dependencies::

       pip install -r requirements.txt

3. Start the service::

       uvicorn app.main:app --reload





