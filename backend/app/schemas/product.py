from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    category: str
    quantity: int  # ✅ Add this field

class ProductOut(ProductCreate):
    id: int
    vendor_id: int

    class Config:
        from_attributes = True
