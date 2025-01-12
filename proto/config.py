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
CREATE_CODE_PORT = os.getenv("CREATE_CODE_PORT")
