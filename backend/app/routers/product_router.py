from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.deps import require_vendor
from app.models.product_model import Product  # ✅ Product model
from app.schemas.product import ProductCreate, ProductOut  # ✅ Schema

router = APIRouter(tags=["Products"])


@router.post("/create", response_model=ProductOut)
def create_product(payload: ProductCreate, db: Session = Depends(get_db), user = Depends(require_vendor)):
    # user is the vendor who is creating the product
    product = Product(
        name=payload.name,
        price=payload.price,
        description=payload.description,
        category=payload.category,
        quantity=payload.quantity,   # ✅ Added this line
        vendor_id=user.id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
