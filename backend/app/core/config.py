import os

from dotenv import load_dotenv

load_dotenv()

# DATABASE CONFIGURATION
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")


# REDIS CONFIGURATION

REDIS_HOST = os.getenv("REDIS_HOST", None)
REDIS_PORT = os.getenv("REDIS_PORT", None)
