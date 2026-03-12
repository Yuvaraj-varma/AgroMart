from fastapi import APIRouter, HTTPException, Request
from app.kafka_producer import send_order_to_kafka
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from uuid import uuid4
from datetime import datetime

router = APIRouter(tags=["Orders"])

# ✅ Pydantic schema to validate order data
class OrderItem(BaseModel):
    product_id: str | int
    name: str
    quantity: int
    price: float

class OrderCreate(BaseModel):
    order_id: str = Field(default_factory=lambda: str(uuid4()))
    buyer_name: str | None = None
    items: List[OrderItem]
    total_price: float
    currency: str = "INR"
    metadata: Dict[str, Any] = {}

# ✅ Route to receive orders and send them to Kafka
@router.post("/create")
async def create_order(order: OrderCreate, request: Request):
    """
    Receives order data from AgroMart frontend,
    sends it to Kafka for MongoDB storage.
    """

    # Add metadata like IP and timestamp
    order_data = order.dict()
    order_data["source_ip"] = request.client.host if request.client else "unknown"
    order_data["created_at"] = datetime.utcnow().isoformat()

    try:
        send_order_to_kafka(order_data)
        return {
            "message": "✅ Order sent to Kafka successfully",
            "order_id": order_data["order_id"]
        }
    except Exception as e:
        print(f"❌ Error sending to Kafka: {e}")
        raise HTTPException(status_code=500, detail="Failed to send order to Kafka")
