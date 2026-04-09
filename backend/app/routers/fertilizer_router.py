from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Security
from sqlalchemy.orm import Session
from app.db.postgres_session import get_db
from app.schemas.fertilizer_schema import FertilizerResponse
from app.services import fertilizer_service
from app.core.security import security, verify_token

router = APIRouter(tags=["Fertilizers"])


def get_optional_vendor_id(credentials=Security(security, scopes=[])):
    try:
        payload = verify_token(credentials)
        if payload.get("role") == "vendor":
            return int(payload.get("sub"))
    except Exception:
        pass
    return None


@router.post("/", response_model=FertilizerResponse)
def create_fertilizer(
    name: str = Form(...),
    type: str = Form(None),
    price: float = Form(None),
    description: str = Form(None),
    farmer_name: str = Form(None),
    location: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    vendor_id: int = Depends(get_optional_vendor_id)
):
    return fertilizer_service.create_fertilizer(db, name, type, price, description, farmer_name, location, image, vendor_id)


@router.get("/", response_model=list[FertilizerResponse])
def get_all_fertilizers(db: Session = Depends(get_db)):
    return fertilizer_service.get_all_fertilizers(db)


@router.get("/{fertilizer_id}", response_model=FertilizerResponse)
def get_fertilizer(fertilizer_id: int, db: Session = Depends(get_db)):
    fertilizer = fertilizer_service.get_fertilizer(db, fertilizer_id)
    if not fertilizer:
        raise HTTPException(status_code=404, detail="Fertilizer not found")
    return fertilizer


@router.put("/{fertilizer_id}", response_model=FertilizerResponse)
def update_fertilizer(
    fertilizer_id: int,
    name: str = Form(None),
    type: str = Form(None),
    price: float = Form(None),
    description: str = Form(None),
    farmer_name: str = Form(None),
    location: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    updated = fertilizer_service.update_fertilizer(db, fertilizer_id, name, type, price, description, farmer_name, location, image)
    if not updated:
        raise HTTPException(status_code=404, detail="Fertilizer not found")
    return updated


@router.delete("/{fertilizer_id}")
def delete_fertilizer(fertilizer_id: int, db: Session = Depends(get_db)):
    deleted = fertilizer_service.delete_fertilizer(db, fertilizer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Fertilizer not found")
    return {"message": f"Fertilizer {fertilizer_id} deleted successfully"}
