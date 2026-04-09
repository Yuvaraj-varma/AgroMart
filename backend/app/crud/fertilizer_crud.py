from sqlalchemy.orm import Session
from app.db.models.fertilizer_model import Fertilizer
from app.schemas.fertilizer_schema import FertilizerCreate


def create_fertilizer(db: Session, fertilizer: FertilizerCreate, image_url: str = None, vendor_id: int = None):
    new_fertilizer = Fertilizer(**fertilizer.model_dump(), image_url=image_url, vendor_id=vendor_id)
    db.add(new_fertilizer)
    db.commit()
    db.refresh(new_fertilizer)
    return new_fertilizer


def get_all_fertilizers(db: Session):
    return db.query(Fertilizer).all()


def get_fertilizers_by_vendor(db: Session, vendor_id: int):
    return db.query(Fertilizer).filter(Fertilizer.vendor_id == vendor_id).all()


def get_fertilizer_by_id(db: Session, fertilizer_id: int):
    return db.query(Fertilizer).filter(Fertilizer.id == fertilizer_id).first()


def update_fertilizer(db: Session, fertilizer_id: int, data: FertilizerCreate, image_url: str = None):
    fertilizer = get_fertilizer_by_id(db, fertilizer_id)
    if not fertilizer:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(fertilizer, key, value)
    if image_url:
        fertilizer.image_url = image_url
    db.commit()
    db.refresh(fertilizer)
    return fertilizer


def delete_fertilizer(db: Session, fertilizer_id: int):
    fertilizer = get_fertilizer_by_id(db, fertilizer_id)
    if not fertilizer:
        return False
    db.delete(fertilizer)
    db.commit()
    return True
