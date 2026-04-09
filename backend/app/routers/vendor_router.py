from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from app.db.postgres_session import get_db
from app.core.security import security, verify_token
from app.crud import crop_crud, seed_crud, fertilizer_crud

router = APIRouter(tags=["Vendor Dashboard"])


def get_vendor_id(credentials=Security(security)):
    payload = verify_token(credentials)
    if payload.get("role") != "vendor":
        raise HTTPException(status_code=403, detail="Vendor access only")
    return int(payload.get("sub"))


@router.get("/my-products")
def get_my_products(vendor_id: int = Depends(get_vendor_id), db: Session = Depends(get_db)):
    crops        = crop_crud.get_crops_by_vendor(db, vendor_id)
    seeds        = seed_crud.get_seeds_by_vendor(db, vendor_id)
    fertilizers  = fertilizer_crud.get_fertilizers_by_vendor(db, vendor_id)

    return {
        "crops":       [{"id": c.id, "name": c.name, "price": c.price, "type": c.type, "image_url": c.image_url, "category": "crops"}       for c in crops],
        "seeds":       [{"id": s.id, "name": s.name, "price": s.price, "type": s.type, "image_url": s.image_url, "category": "seeds"}       for s in seeds],
        "fertilizers": [{"id": f.id, "name": f.name, "price": f.price, "type": f.type, "image_url": f.image_url, "category": "fertilizers"} for f in fertilizers],
    }


@router.delete("/my-products/{category}/{product_id}")
def delete_my_product(
    category: str,
    product_id: int,
    vendor_id: int = Depends(get_vendor_id),
    db: Session = Depends(get_db)
):
    if category == "crops":
        product = crop_crud.get_crop_by_id(db, product_id)
        delete_fn = crop_crud.delete_crop
    elif category == "seeds":
        product = seed_crud.get_seed_by_id(db, product_id)
        delete_fn = seed_crud.delete_seed
    elif category == "fertilizers":
        product = fertilizer_crud.get_fertilizer_by_id(db, product_id)
        delete_fn = fertilizer_crud.delete_fertilizer
    else:
        raise HTTPException(status_code=400, detail="Invalid category")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.vendor_id != vendor_id:
        raise HTTPException(status_code=403, detail="You can only delete your own products")

    delete_fn(db, product_id)
    return {"message": f"✅ {category[:-1].capitalize()} deleted successfully"}
