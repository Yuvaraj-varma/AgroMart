from sqlalchemy.orm import Session
from app.models.crop_model import Crop
from app.schemas.crop_schema import CropCreate

def create_crop(db: Session, crop: CropCreate, image_url: str = None):
    new_crop = Crop(**crop.model_dump(), image_url=image_url)
    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)
    return new_crop

def get_all_crops(db: Session):
    return db.query(Crop).all()

def get_crop_by_id(db: Session, crop_id: int):
    return db.query(Crop).filter(Crop.id == crop_id).first()

def update_crop(db: Session, crop_id: int, data: CropCreate, image_url: str = None):
    crop = get_crop_by_id(db, crop_id)
    if not crop:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(crop, key, value)
    if image_url:
        crop.image_url = image_url
    db.commit()
    db.refresh(crop)
    return crop

def delete_crop(db: Session, crop_id: int):
    crop = get_crop_by_id(db, crop_id)
    if not crop:
        return False
    db.delete(crop)
    db.commit()
    return True
