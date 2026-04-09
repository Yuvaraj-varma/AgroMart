"""
FULL MONGODB COLLECTION SETUP FILE
=====================================
Run this file ONCE to create all collections + indexes:

    python mongo_models.py

It will:
- Connect to MongoDB
- Create ALL collections
- Create ALL indexes
- Insert sample validator schemas
"""

import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from pymongo import MongoClient, ASCENDING, DESCENDING
from app.db.config import MONGODB_URL

# ==========================================================
# DATABASE CONNECTION
# ==========================================================

client = MongoClient(MONGODB_URL)
db = client["liveRatesDB"]


# ==========================================================
# COLLECTION DEFINITIONS + INDEXES
# ==========================================================

# ----------------------------------------------------------
# rates — daily market rates from Agmarknet API
# Document shape:
# {
#   date        : "2024-01-15",
#   fetched_at  : datetime,
#   count       : int,
#   crops       : [ { commodity, commodity_norm, max_price, min_price, modal_price, market, state } ],
#   seeds       : [ { commodity, commodity_norm, max_price, min_price, modal_price, market, state } ]
# }
# ----------------------------------------------------------

rates = db["rates"]
rates.create_index([("date", DESCENDING)], unique=True)
rates.create_index([("fetched_at", DESCENDING)])


# ----------------------------------------------------------
# orders — Kafka-consumed orders stored in MongoDB
# Document shape:
# {
#   order_id       : "uuid",
#   buyer_name     : "string",
#   items          : [ { product_id, name, quantity, price } ],
#   total_price    : float,
#   currency       : "INR",
#   payment_method : "UPI" | "Bank Transfer" | "Cash on Delivery",
#   status         : "pending" | "confirmed" | "shipped" | "delivered" | "cancelled",
#   source_ip      : "string",
#   created_at     : datetime
# }
# ----------------------------------------------------------

orders = db["orders"]
orders.create_index([("order_id", ASCENDING)], unique=True)
orders.create_index([("created_at", DESCENDING)])
orders.create_index([("status", ASCENDING)])


# ----------------------------------------------------------
# price_history — historical commodity price snapshots
# Document shape:
# {
#   commodity      : "Rice",
#   commodity_norm : "rice",
#   date           : "2024-01-15",
#   max_price      : float,
#   min_price      : float,
#   modal_price    : float,
#   market         : "Delhi",
#   state          : "Delhi"
# }
# ----------------------------------------------------------

price_history = db["price_history"]
price_history.create_index([("commodity_norm", ASCENDING), ("date", DESCENDING)])
price_history.create_index([("date", DESCENDING)])


# ==========================================================
# RUN DIRECTLY — creates all collections + indexes
# ==========================================================

if __name__ == "__main__":
    print("Connecting to:", MONGODB_URL)
    try:
        collections = ["rates", "orders", "price_history"]

        for name in collections:
            if name not in db.list_collection_names():
                db.create_collection(name)
                print(f"   ✅ Created collection: {name}")
            else:
                print(f"   ⚠️  Already exists:    {name}")

        # Re-apply indexes
        rates.create_index([("date", DESCENDING)], unique=True)
        rates.create_index([("fetched_at", DESCENDING)])

        orders.create_index([("order_id", ASCENDING)], unique=True)
        orders.create_index([("created_at", DESCENDING)])
        orders.create_index([("status", ASCENDING)])

        price_history.create_index([("commodity_norm", ASCENDING), ("date", DESCENDING)])
        price_history.create_index([("date", DESCENDING)])

        print("\n✅ MongoDB setup completed successfully!")
        print("✅ Collections ready:")
        for col in db.list_collection_names():
            print(f"   - {col}")

    except Exception as e:
        print("❌ MongoDB setup failed:", e)
        sys.exit(1)
