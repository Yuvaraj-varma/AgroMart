from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import database
from app.crud import seed_crud
from app.schemas.seed_schema import SeedResponse, SeedCreate
import os, shutil

router = APIRouter(tags=["Seeds"])
get_db = database.get_db

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ➕ Create new seed (farmer_name/location can be filled or empty)
@router.post("/", response_model=SeedResponse)
def create_seed(
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

    data = SeedCreate(
        name=name,
        type=type,
        price=price,
        description=description,
        farmer_name=farmer_name or "",
        location=location or ""
    )
    return seed_crud.create_seed(db, data, image_url)

# 📜 Get all seeds
@router.get("/", response_model=list[SeedResponse])
def get_all_seeds(db: Session = Depends(get_db)):
    return seed_crud.get_all_seeds(db)

# 🔍 Get single seed by ID
@router.get("/{seed_id}", response_model=SeedResponse)
def get_seed(seed_id: int, db: Session = Depends(get_db)):
    seed = seed_crud.get_seed_by_id(db, seed_id)
    if not seed:
        raise HTTPException(status_code=404, detail="Seed not found")
    return seed

# ✏️ Update seed (farmer_name/location stored but hidden in frontend)
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
    image_url = None
    if image:
        image_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/{UPLOAD_DIR}/{image.filename}"

    data = SeedCreate(
        name=name,
        type=type,
        price=price,
        description=description,
        farmer_name=farmer_name or "",
        location=location or ""
    )

    updated = seed_crud.update_seed(db, seed_id, data, image_url)
    if not updated:
        raise HTTPException(status_code=404, detail="Seed not found")
    return updated

# 🗑️ Delete seed
@router.delete("/{seed_id}")
def delete_seed(seed_id: int, db: Session = Depends(get_db)):
    deleted = seed_crud.delete_seed(db, seed_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Seed not found")
    return {"message": f"🗑️ Seed with id {seed_id} deleted successfully"}
