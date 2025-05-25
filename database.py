import weaviate
from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGO_DB_URL, WEAVIATE_URL

__mongo_client = AsyncIOMotorClient(MONGO_DB_URL)
__mongo_db = __mongo_client["arxiv"]
mongo_collection = __mongo_db["papers"]

weaviate_client = weaviate.Client(url=WEAVIATE_URL)
