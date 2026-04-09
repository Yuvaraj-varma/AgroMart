from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.postgres_session import get_db
from app.db.models.user_model import Buyer, Vendor
from app.core.security import security
from app.core.config import settings


def get_current_user(credentials=Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role not in ["buyer", "vendor"]:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Buyer).filter(Buyer.id == user_id).first() if role == "buyer" \
        else db.query(Vendor).filter(Vendor.id == user_id).first()

    if not user:
        raise credentials_exception
    return user


def require_vendor(current_user=Depends(get_current_user)):
    if not isinstance(current_user, Vendor):
        raise HTTPException(status_code=403, detail="Vendor access only")
    return current_user


def require_buyer(current_user=Depends(get_current_user)):
    if not isinstance(current_user, Buyer):
        raise HTTPException(status_code=403, detail="Buyer access only")
    return current_user
