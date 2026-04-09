import os
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.crud import crop_crud
from app.schemas.crop_schema import CropCreate

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(image: UploadFile) -> str:
    image_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return f"/{UPLOAD_DIR}/{image.filename}"


def create_crop(db: Session, name: str, type: str, price: float,
                description: str, farmer_name: str, location: str,
                image: UploadFile = None):
    image_url = save_image(image) if image else None
    data = CropCreate(name=name, type=type, price=price,
                      description=description,
                      farmer_name=farmer_name or "",
                      location=location or "")
    return crop_crud.create_crop(db, data, image_url)


def get_all_crops(db: Session):
    return crop_crud.get_all_crops(db)


def get_crop(db: Session, crop_id: int):
    return crop_crud.get_crop_by_id(db, crop_id)


def update_crop(db: Session, crop_id: int, name: str, type: str, price: float,
                description: str, farmer_name: str, location: str,
                image: UploadFile = None):
    image_url = save_image(image) if image else None
    data = CropCreate(name=name, type=type, price=price,
                      description=description,
                      farmer_name=farmer_name or "",
                      location=location or "")
    return crop_crud.update_crop(db, crop_id, data, image_url)


def delete_crop(db: Session, crop_id: int):
    return crop_crud.delete_crop(db, crop_id)
