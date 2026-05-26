import os

from dotenv import load_dotenv

load_dotenv()

# DATABASE CONFIGURATION
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
