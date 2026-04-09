from pydantic import BaseModel, field_validator
from typing import Optional


class FertilizerBase(BaseModel):
    name: str
    type: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

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
        if v is not None and v <= 0:
            raise ValueError("Price must be greater than 0")
        return v

    @field_validator("description")
    def validate_description(cls, v):
        if v is not None and len(v.strip()) < 5:
            raise ValueError("Description must be at least 5 characters")
        return v


class FertilizerCreate(FertilizerBase):
    farmer_name: Optional[str] = None
    location: Optional[str] = None


class FertilizerResponse(FertilizerBase):
    id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
