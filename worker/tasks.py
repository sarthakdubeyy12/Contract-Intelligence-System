import os
import json
import asyncio
import logging
from celery import shared_task
from motor.motor_asyncio import AsyncIOMotorClient
from contract_parser import parse_contract  # ✅ ML/NLP parser module

# ---------- Logging ----------
logger = logging.getLogger(__name__)

# ---------- Mongo Config ----------
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "contracts_db")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "contracts")


# ---------- Mongo Helper ----------
async def save_to_mongo(contract_id: str, parsed_data: dict, status: str = "completed"):
    """
    Save parsed contract results (or errors) to MongoDB.
    """
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    await collection.update_one(
        {"contract_id": contract_id},  # search by contract_id
        {"$set": {"parsed_data": parsed_data, "status": status}},
        upsert=True,
    )
    client.close()


# ---------- Celery Task ----------
@shared_task(
    name="parse_contract",
    bind=True,  # needed to use self.retry
    autoretry_for=(Exception,),  # automatically retry on any Exception
    retry_kwargs={"max_retries": 3, "countdown": 10},  # retry 3x with 10s delay
    retry_backoff=True,  # exponential backoff (10s, 20s, 40s...)
)
def parse_contract_task(self, file_path: str, contract_id: str):
    """
    Celery task:
    1. Parse uploaded contract with ML/NLP.
    2. Store extracted results locally (JSON).
    3. Persist results in MongoDB.
    Retries automatically on failure.
    """
    try:
        # Step 1: Parse contract
        parsed_data = parse_contract(file_path, contract_id)

        # Step 2: Save results locally
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        results_dir = os.path.join(base_dir, "results")
        os.makedirs(results_dir, exist_ok=True)

        result_path = os.path.join(results_dir, f"{contract_id}.json")
        with open(result_path, "w") as f:
            json.dump(parsed_data, f, indent=2)

        # Step 3: Save results in MongoDB
        asyncio.run(save_to_mongo(contract_id, parsed_data, status="completed"))

        logger.info(f"✅ Contract {contract_id} parsed successfully.")
        return {"status": "completed", "path": result_path}

    except Exception as e:
        error_message = str(e)
        logger.error(f"❌ Error parsing contract {contract_id}: {error_message}")

        # Save error to Mongo
        try:
            asyncio.run(save_to_mongo(contract_id, {"error": error_message}, status="failed"))
        except Exception as mongo_err:
            logger.error(f"❌ Failed to save error in MongoDB: {mongo_err}")

        # Retry the task (up to max_retries)
        raise self.retry(exc=e)