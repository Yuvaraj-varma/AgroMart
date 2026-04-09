from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.crop_schema import CropResponse
from app.services import crop_service

router = APIRouter(tags=["Crops"])


@router.post("/", response_model=CropResponse)
def create_crop(
    name: str = Form(...),
    type: str = Form(None),
    price: float = Form(None),
    description: str = Form(None),
    farmer_name: str = Form(None),
    location: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    return crop_service.create_crop(db, name, type, price, description, farmer_name, location, image)


@router.get("/", response_model=list[CropResponse])
def get_all_crops(db: Session = Depends(get_db)):
    return crop_service.get_all_crops(db)


@router.get("/{crop_id}", response_model=CropResponse)
def get_crop(crop_id: int, db: Session = Depends(get_db)):
    crop = crop_service.get_crop(db, crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop


@router.put("/{crop_id}", response_model=CropResponse)
def update_crop(
    crop_id: int,
    name: str = Form(None),
    type: str = Form(None),
    price: float = Form(None),
    description: str = Form(None),
    farmer_name: str = Form(None),
    location: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    updated = crop_service.update_crop(db, crop_id, name, type, price, description, farmer_name, location, image)
    if not updated:
        raise HTTPException(status_code=404, detail="Crop not found")
    return updated


@router.delete("/{crop_id}")
def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    deleted = crop_service.delete_crop(db, crop_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Crop not found")
    return {"message": f"Crop {crop_id} deleted successfully"}
