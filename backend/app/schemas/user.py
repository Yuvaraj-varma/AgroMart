from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Literal["buyer", "vendor"]

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        if len(v) > 100:
            raise ValueError("Name must be less than 100 characters")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        if len(v) > 100:
            raise ValueError("Password too long")
        return v


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
