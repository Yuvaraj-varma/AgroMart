from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.database import get_db
from app.models.user_model import Vendor, Buyer
from app.schemas.user import UserCreate, UserOut, Token
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_token,
    security,
)

router = APIRouter(tags=["Auth"])

# ✅ Signup route (auto decides Buyer or Vendor table)
@router.post("/signup", response_model=UserOut)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    if payload.role not in ("buyer", "vendor"):
        raise HTTPException(status_code=400, detail="Role must be 'buyer' or 'vendor'")

    # ✅ Prevent duplicate email across both tables (case-insensitive)
    existing_vendor = db.query(Vendor).filter(Vendor.email.ilike(payload.email)).first()
    existing_buyer = db.query(Buyer).filter(Buyer.email.ilike(payload.email)).first()
    if existing_vendor or existing_buyer:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = get_password_hash(payload.password)

    # ✅ Insert into correct table
    if payload.role == "vendor":
        user = Vendor(name=payload.name, email=payload.email.lower(), password=hashed_pwd)
    else:
        user = Buyer(name=payload.name, email=payload.email.lower(), password=hashed_pwd)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": payload.role,
    }


# ✅ Login route (checks both tables automatically & safely)
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email_input = form_data.username.strip().lower()

    # 🔍 Check both tables first
    vendor_user = db.query(Vendor).filter(Vendor.email.ilike(email_input)).first()
    buyer_user = db.query(Buyer).filter(Buyer.email.ilike(email_input)).first()

    # 🛑 Prevent same email existing in both tables
    if vendor_user and buyer_user:
        raise HTTPException(
            status_code=400,
            detail="Duplicate email found in both Buyer and Vendor tables. Please contact support.",
        )

    # ✅ Vendor login
    if vendor_user:
        if not verify_password(form_data.password, vendor_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        role = "vendor"
        user = vendor_user

    # ✅ Buyer login
    elif buyer_user:
        if not verify_password(form_data.password, buyer_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        role = "buyer"
        user = buyer_user

    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 🔐 Create access token with role
    token_data = {"sub": str(user.id), "role": role}
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(token_data, expires_delta=access_token_expires)

    print(f"✅ Login success → {user.email} as {role}")

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role,
    }


# ✅ Token verification route (returns full user info)
@router.get("/me")
def get_current_user(credentials=Security(security), db: Session = Depends(get_db)):
    """
    ✅ Decode JWT token and return user's full info (id, name, email, role)
    """
    payload = verify_token(credentials)
    user_id = payload.get("sub")
    role = payload.get("role")

    if not user_id or not role:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 🔹 Get user from correct table
    if role == "vendor":
        user = db.query(Vendor).filter(Vendor.id == int(user_id)).first()
    else:
        user = db.query(Buyer).filter(Buyer.id == int(user_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "role": role,
        "token_valid": True,
    }
