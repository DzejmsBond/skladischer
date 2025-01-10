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
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_URL = os.getenv("RAPIDAPI_URL")

# QR Code parameters.
SIZE = "300x300"