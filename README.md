
# Overview

The **Skladischer Management System** is a flexible platform designed to help individuals efficiently record,
annotate, and manage products across various storage spaces. The system offers detailed product information
accessible via the web, enabling users to search by name, filter by date, and review stored items seamlessly.
Each product is assigned a **unique code** upon creation, facilitating precise identification and retrieval.
Supported codes include **barcodes**, **QR codes**, and custom string identifiers.

# Architecture

The system follows a **microservice architecture**, where each service operates independently and
communicates via multiple REST and RPC protocols. Click on the microservice title to see full documentation:

- **[Storage Management Service](http://34.144.195.148/users/docs):** Handles user creation, retrieval, modification and deletion of users, storages and items. This is the application core as it provides the main functionality.
- **[Admin Management Service](http://34.144.195.148/credentials/docs):** Manages user accounts and other user dependant data.
- **[Sensor Management Service](http://34.144.195.148/sensors/docs):** Similarly, to storage managment it manages users automated sensors.
- **[QR Code Management Service](http://34.144.195.148/codes/docs):** Generates and manages product barcodes on creation.

Each microservice is backed by its own **MongoDB database**, ensuring data isolation and consistency.


# Use Cases

- **Freezer Inventory Management:** Managing freezer contents is often challenging due to limited visibility, inconsistent organization, and temperature sensitivity. Our application simplifies this by assigning each product a unique **QR code**, allowing users to quickly identify items without unnecessary handling. The system also maintains a clear overview of all stored items, including expiration dates, quantities, and storage conditions, ensuring better inventory control and reduced waste.

- **Workshop Tool Tracking:** Keeping track of tools in a busy workshop environment can be chaotic, especially when tools are frequently borrowed, returned, or misplaced. With our application, every tool can be tracked with relevant attributes such as **location**, **current user**, and **tool condition**. This ensures that tools are always accounted for, reducing the risk of loss or damage and increasing overall efficiency in workshop operations.

- **Shopping Assistance:** Ever forgotten whether you still have a key ingredient while shopping? With our application, users can remotely **access real-time storage content** from their mobile devices. By checking available items and quantities directly from the app, grocery shopping becomes more efficient, reducing unnecessary purchases and avoiding duplicate items. Additionally, the system can suggest shopping lists based on current storage inventory.