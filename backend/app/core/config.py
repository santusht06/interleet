import os
from pathlib import Path


from dotenv import load_dotenv

load_dotenv()

PROJECT_ENVIRONMENT = "DEVELOPMENT"

# DATABASE CONFIGURATION
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")


# REDIS CONFIGURATION

REDIS_HOST = os.getenv("REDIS_HOST", None)
REDIS_PORT = os.getenv("REDIS_PORT", None)


# JWT
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRES = int(os.getenv("JWT_EXPIRES", 7))
