from sqlalchemy.orm import Session
from app.db.models.seed_model import Seed
from app.schemas.seed_schema import SeedCreate


def create_seed(db: Session, seed: SeedCreate, image_url: str = None, vendor_id: int = None):
    new_seed = Seed(
        name=seed.name, type=seed.type, price=seed.price,
        description=seed.description, farmer_name=seed.farmer_name,
        location=seed.location, image_url=image_url, vendor_id=vendor_id
    )
    db.add(new_seed)
    db.commit()
    db.refresh(new_seed)
    return new_seed


def get_all_seeds(db: Session):
    return db.query(Seed).all()


def get_seeds_by_vendor(db: Session, vendor_id: int):
    return db.query(Seed).filter(Seed.vendor_id == vendor_id).all()


def get_seed_by_id(db: Session, seed_id: int):
    return db.query(Seed).filter(Seed.id == seed_id).first()


def update_seed(db: Session, seed_id: int, updated_data: SeedCreate, image_url: str = None):
    seed = db.query(Seed).filter(Seed.id == seed_id).first()
    if not seed:
        return None
    for key, value in updated_data.model_dump(exclude_unset=True).items():
        setattr(seed, key, value)
    if image_url:
        seed.image_url = image_url
    db.commit()
    db.refresh(seed)
    return seed


def delete_seed(db: Session, seed_id: int):
    seed = db.query(Seed).filter(Seed.id == seed_id).first()
    if not seed:
        return False
    db.delete(seed)
    db.commit()
    return True
