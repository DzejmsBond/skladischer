# Author: Nina Mislej
# Date created: 07.01.2025

from pathlib import Path
from dotenv import load_dotenv
import os

# Enable if manual loading of environment variables is needed.
# In general avoid this to avoid git conflicts.
# CODE: ENV_PATH = Path(__file__).resolve().parent.parent / 'config.env'
#       load_dotenv(dotenv_path=ENV_PATH)

# Access variables.
MONGO_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION = os.getenv("COLLECTION")

# Other microservices communiacting over RPC.
CODES_MS_HOST = os.getenv("CODES_MS_HOST")

# Authorization.
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

GOOGLE_CLOUD_LOGGING = os.getenv("GOOGLE_CLOUD_LOGGING")