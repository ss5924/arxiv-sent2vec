import os

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
WEAVIATE_URL = os.getenv("WEAVIATE_URL")

MAX_CONCURRENT_TASKS = 4
BATCH_SIZE = 100
