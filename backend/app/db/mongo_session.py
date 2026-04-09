from pymongo import MongoClient
from app.db.config import MONGODB_URL

if not MONGODB_URL:
    raise RuntimeError(
        "No MongoDB configuration found. Set MONGODB_URL in the .env file."
    )

client = MongoClient(MONGODB_URL)
mongo_db = client["liveRatesDB"]

# Collections
rates_collection    = mongo_db["rates"]
orders_collection   = mongo_db["orders"]
history_collection  = mongo_db["price_history"]


def get_mongo_db():
    """
    Dependency for FastAPI routes that need MongoDB.
    Usage: db = Depends(get_mongo_db)
    """
    try:
        yield mongo_db
    except Exception as e:
        print(f"Error in MongoDB operation: {e}")
        raise


def create_collections():
    """
    Create MongoDB collections and indexes.
    Call this once during FastAPI startup.
    """
    try:
        import app.db.mongo_models as models  # noqa: F401
    except Exception as e:
        print(f"Could not import mongo_models: {e}")
        raise

    try:
        models.setup_indexes()
        print("✅ MongoDB collections and indexes created successfully.")
    except Exception as e:
        print(f"❌ Error creating MongoDB collections: {e}")
        raise
