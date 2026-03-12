from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import database
from app.crud import crop_crud
from app.schemas.crop_schema import CropResponse, CropCreate
import os, shutil

# ⬅️ Removed prefix="/crops" to prevent double prefix issue
router = APIRouter(tags=["Crops"])
get_db = database.get_db

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ➕ Create new crop
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
    image_url = None
    if image:
        image_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/{UPLOAD_DIR}/{image.filename}"

    data = CropCreate(
        name=name,
        type=type,
        price=price,
        description=description,
        farmer_name=farmer_name or "",
        location=location or ""
    )

    return crop_crud.create_crop(db, data, image_url)


# 📜 Get all crops
@router.get("/", response_model=list[CropResponse])
def get_all_crops(db: Session = Depends(get_db)):
    return crop_crud.get_all_crops(db)


# 🔍 Get single crop by ID
@router.get("/{crop_id}", response_model=CropResponse)
def get_crop(crop_id: int, db: Session = Depends(get_db)):
    crop = crop_crud.get_crop_by_id(db, crop_id)
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    return crop


# ✏️ Update crop
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
    image_url = None
    if image:
        image_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/{UPLOAD_DIR}/{image.filename}"

    data = CropCreate(
        name=name,
        type=type,
        price=price,
        description=description,
        farmer_name=farmer_name or "",
        location=location or ""
    )

    updated = crop_crud.update_crop(db, crop_id, data, image_url)
    if not updated:
        raise HTTPException(status_code=404, detail="Crop not found")
    return updated


# 🗑️ Delete crop
@router.delete("/{crop_id}")
def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    deleted = crop_crud.delete_crop(db, crop_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Crop not found")
    return {"message": f"🗑️ Crop with id {crop_id} deleted successfully"}
