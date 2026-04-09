import os
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.crud import fertilizer_crud
from app.schemas.fertilizer_schema import FertilizerCreate

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(image: UploadFile) -> str:
    image_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return f"/{UPLOAD_DIR}/{image.filename}"


def create_fertilizer(db: Session, name: str, type: str, price: float,
                      description: str, farmer_name: str, location: str,
                      image: UploadFile = None, vendor_id: int = None):
    image_url = save_image(image) if image else None
    data = FertilizerCreate(name=name, type=type, price=price,
                            description=description,
                            farmer_name=farmer_name or "",
                            location=location or "")
    return fertilizer_crud.create_fertilizer(db, data, image_url, vendor_id)


def get_all_fertilizers(db: Session):
    return fertilizer_crud.get_all_fertilizers(db)


def get_fertilizer(db: Session, fertilizer_id: int):
    return fertilizer_crud.get_fertilizer_by_id(db, fertilizer_id)


def update_fertilizer(db: Session, fertilizer_id: int, name: str, type: str,
                      price: float, description: str, farmer_name: str,
                      location: str, image: UploadFile = None):
    image_url = save_image(image) if image else None
    data = FertilizerCreate(name=name, type=type, price=price,
                            description=description,
                            farmer_name=farmer_name or "",
                            location=location or "")
    return fertilizer_crud.update_fertilizer(db, fertilizer_id, data, image_url)


def delete_fertilizer(db: Session, fertilizer_id: int):
    return fertilizer_crud.delete_fertilizer(db, fertilizer_id)
