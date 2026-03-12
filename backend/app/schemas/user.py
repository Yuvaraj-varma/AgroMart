from pydantic import BaseModel, EmailStr


# ✅ Common schema for signup
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # either "vendor" or "buyer"


# ✅ Common output schema
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True  # use this instead of orm_mode in Pydantic v2


# ✅ Token schema (used for login)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
