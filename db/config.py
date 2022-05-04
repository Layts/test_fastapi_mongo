from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from config import settings


engine = AIOEngine(motor_client=AsyncIOMotorClient(), database=settings.db_name)