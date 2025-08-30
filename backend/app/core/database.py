# backend/app/core/database.py
import motor.motor_asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# Create MongoDB client (global)
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

def get_database():
    """Return the MongoDB database instance."""
    return db

async def check_connection():
    """Ping the MongoDB server to check connection."""
    try:
        await client.admin.command("ping")
        print("✅ MongoDB connection successful!")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)

def close_connection():
    """Close MongoDB client."""
    client.close()
    print("👋 MongoDB connection closed")