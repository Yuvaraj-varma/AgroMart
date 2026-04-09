import os
import shutil
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.crud import seed_crud
from app.schemas.seed_schema import SeedCreate

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(image: UploadFile) -> str:
    image_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return f"/{UPLOAD_DIR}/{image.filename}"


def create_seed(db: Session, name: str, type: str, price: float,
                description: str, farmer_name: str, location: str,
                image: UploadFile = None, vendor_id: int = None):
    image_url = save_image(image) if image else None
    data = SeedCreate(name=name, type=type, price=price,
                      description=description,
                      farmer_name=farmer_name or "",
                      location=location or "")
    return seed_crud.create_seed(db, data, image_url, vendor_id)


def get_all_seeds(db: Session):
    return seed_crud.get_all_seeds(db)


def get_seed(db: Session, seed_id: int):
    return seed_crud.get_seed_by_id(db, seed_id)


def update_seed(db: Session, seed_id: int, name: str, type: str, price: float,
                description: str, farmer_name: str, location: str,
                image: UploadFile = None):
    image_url = save_image(image) if image else None
    data = SeedCreate(name=name, type=type, price=price,
                      description=description,
                      farmer_name=farmer_name or "",
                      location=location or "")
    return seed_crud.update_seed(db, seed_id, data, image_url)


def delete_seed(db: Session, seed_id: int):
    return seed_crud.delete_seed(db, seed_id)
