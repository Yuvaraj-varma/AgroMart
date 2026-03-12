from pydantic import BaseModel
from typing import Optional

# 🌱 Base schema (shared fields)
class SeedBase(BaseModel):
    name: str
    type: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


# 🧩 Used when creating a new seed (backend stores farmer/location)
class SeedCreate(SeedBase):
    farmer_name: Optional[str] = None
    location: Optional[str] = None


# 📤 Response model for frontend (farmer/location hidden)
class SeedResponse(SeedBase):
    id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True  # ✅ replaces orm_mode=True in Pydantic v2
