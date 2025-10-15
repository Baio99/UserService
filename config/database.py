from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect_db(cls):
        """Conectar a MongoDB"""
        mongodb_uri = os.getenv("MONGODB_URI")
        cls.client = AsyncIOMotorClient(mongodb_uri)
        print("✅ Conectado a MongoDB")
    
    @classmethod
    async def close_db(cls):
        """Cerrar conexión a MongoDB"""
        if cls.client:
            cls.client.close()
            print("❌ Conexión a MongoDB cerrada")
    
    @classmethod
    def get_database(cls):
        """Obtener base de datos"""
        database_name = os.getenv("DATABASE_NAME", "users_db")
        return cls.client[database_name]
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Obtener colección"""
        db = cls.get_database()
        return db[collection_name]