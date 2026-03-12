from pydantic import BaseModel
from typing import Optional

# 🌿 Base schema (shared fields)
class FertilizerBase(BaseModel):
    name: str
    type: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


# 🧩 Used when creating a new fertilizer (backend stores farmer/location)
class FertilizerCreate(FertilizerBase):
    farmer_name: Optional[str] = None
    location: Optional[str] = None


# 📤 Response model for frontend (farmer/location hidden)
class FertilizerResponse(FertilizerBase):
    id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True  # ✅ replaces orm_mode=True in Pydantic v2


