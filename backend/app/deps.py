from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import Buyer, Vendor   # ✅ fixed import
from app.core.security import security
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def get_current_user(credentials=Depends(security), db: Session = Depends(get_db)):
    """✅ Extract user info (buyer/vendor) from token"""
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role not in ["buyer", "vendor"]:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # ✅ Check which table to query based on role
    if role == "buyer":
        user = db.query(Buyer).filter(Buyer.id == user_id).first()
    else:
        user = db.query(Vendor).filter(Vendor.id == user_id).first()

    if not user:
        raise credentials_exception

    return user


def require_vendor(current_user=Depends(get_current_user)):
    """✅ Allow only vendors"""
    if not isinstance(current_user, Vendor):
        raise HTTPException(status_code=403, detail="Vendor access only")
    return current_user


def require_buyer(current_user=Depends(get_current_user)):
    """✅ Allow only buyers"""
    if not isinstance(current_user, Buyer):
        raise HTTPException(status_code=403, detail="Buyer access only")
    return current_user
