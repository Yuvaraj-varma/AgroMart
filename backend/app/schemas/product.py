from pydantic import BaseModel, field_validator


class ProductCreate(BaseModel):
    name: str
    price: float
    description: str
    category: str
    quantity: int

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        if len(v) > 100:
            raise ValueError("Name must be less than 100 characters")
        return v

    @field_validator("price")
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @field_validator("quantity")
    def validate_quantity(cls, v):
        if v < 0:
            raise ValueError("Quantity cannot be negative")
        return v

    @field_validator("description")
    def validate_description(cls, v):
        if len(v.strip()) < 5:
            raise ValueError("Description must be at least 5 characters")
        return v


class ProductOut(ProductCreate):
    id: int
    vendor_id: int

    class Config:
        from_attributes = True
