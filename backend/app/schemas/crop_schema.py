from pydantic import BaseModel
from typing import Optional

# 🧾 Base schema (used for shared fields)
class CropBase(BaseModel):
    name: str
    type: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


# 🪴 Used when creating a new crop (includes hidden backend-only fields)
class CropCreate(CropBase):
    farmer_name: Optional[str] = None
    location: Optional[str] = None


# 📤 Used for sending data to frontend (no farmer/location)
class CropResponse(CropBase):
    id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True  # ✅ replaces orm_mode=True in Pydantic v2
