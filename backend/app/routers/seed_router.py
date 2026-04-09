from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Security
from sqlalchemy.orm import Session
from app.db.postgres_session import get_db
from app.schemas.seed_schema import SeedResponse
from app.services import seed_service
from app.core.security import security, verify_token

router = APIRouter(tags=["Seeds"])


def get_optional_vendor_id(credentials=Security(security, scopes=[])):
    try:
        payload = verify_token(credentials)
        if payload.get("role") == "vendor":
            return int(payload.get("sub"))
    except Exception:
        pass
    return None


@router.post("/", response_model=SeedResponse)
def create_seed(
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
    return seed_service.create_seed(db, name, type, price, description, farmer_name, location, image, vendor_id)


@router.get("/", response_model=list[SeedResponse])
def get_all_seeds(db: Session = Depends(get_db)):
    return seed_service.get_all_seeds(db)


@router.get("/{seed_id}", response_model=SeedResponse)
def get_seed(seed_id: int, db: Session = Depends(get_db)):
    seed = seed_service.get_seed(db, seed_id)
    if not seed:
        raise HTTPException(status_code=404, detail="Seed not found")
    return seed


@router.put("/{seed_id}", response_model=SeedResponse)
def update_seed(
    seed_id: int,
    name: str = Form(None),
    type: str = Form(None),
    price: float = Form(None),
    description: str = Form(None),
    farmer_name: str = Form(None),
    location: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    updated = seed_service.update_seed(db, seed_id, name, type, price, description, farmer_name, location, image)
    if not updated:
        raise HTTPException(status_code=404, detail="Seed not found")
    return updated


@router.delete("/{seed_id}")
def delete_seed(seed_id: int, db: Session = Depends(get_db)):
    deleted = seed_service.delete_seed(db, seed_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Seed not found")
    return {"message": f"Seed {seed_id} deleted successfully"}
