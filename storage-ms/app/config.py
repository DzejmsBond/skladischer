# Author: Nina Mislej
# Date created: 07.01.2025

from pathlib import Path
from dotenv import load_dotenv
import os

# TODO: This should not be in the production version?
#       Is this the best way to do this?
# Commented out to pass environment variables in the proper way
#ENV_PATH = Path(__file__).resolve().parent.parent / 'config.env'
#load_dotenv(dotenv_path=ENV_PATH)

# Access variables.
MONGO_URL = os.getenv("DATABASE_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION = os.getenv("COLLECTION")