# Author: Nina Mislej
# Date created: 07.01.2025

from pathlib import Path
from dotenv import load_dotenv
import os

# Enable if manual loading of environment variables is needed.
# In general avoid this to avoid git conflicts.
# CODE: ENV_PATH = Path(__file__).resolve().parent.parent / 'config.env'
#       load_dotenv(dotenv_path=ENV_PATH)

# Port variables.
PORT_CODE = os.getenv("PORT_CODE")
PORT_SENSOR = os.getenv("PORT_SENSOR")
PORT_STORAGE = os.getenv("PORT_STORAGE")
