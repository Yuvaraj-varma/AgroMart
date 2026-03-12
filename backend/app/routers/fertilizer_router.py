from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app import database
from app.crud import fertilizer_crud
from app.schemas.fertilizer_schema import FertilizerResponse, FertilizerCreate
import os, shutil

router = APIRouter(tags=["Fertilizers"])
get_db = database.get_db

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ➕ Create new fertilizer
@router.post("/", response_model=FertilizerResponse)
def create_fertilizer(
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

    data = FertilizerCreate(
        name=name,
        type=type,
        price=price,
        description=description,
        farmer_name=farmer_name or "",
        location=location or ""
    )
    return fertilizer_crud.create_fertilizer(db, data, image_url)

# 📜 Get all fertilizers
@router.get("/", response_model=list[FertilizerResponse])
def get_all_fertilizers(db: Session = Depends(get_db)):
    return fertilizer_crud.get_all_fertilizers(db)

# 🔍 Get one fertilizer
@router.get("/{fertilizer_id}", response_model=FertilizerResponse)
def get_fertilizer(fertilizer_id: int, db: Session = Depends(get_db)):
    fertilizer = fertilizer_crud.get_fertilizer_by_id(db, fertilizer_id)
    if not fertilizer:
        raise HTTPException(status_code=404, detail="Fertilizer not found")
    return fertilizer

# ✏️ Update fertilizer
@router.put("/{fertilizer_id}", response_model=FertilizerResponse)
def update_fertilizer(
    fertilizer_id: int,
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

    data = FertilizerCreate(
        name=name,
        type=type,
        price=price,
        description=description,
        farmer_name=farmer_name or "",
        location=location or ""
    )

    updated = fertilizer_crud.update_fertilizer(db, fertilizer_id, data, image_url)
    if not updated:
        raise HTTPException(status_code=404, detail="Fertilizer not found")
    return updated

# 🗑️ Delete fertilizer
@router.delete("/{fertilizer_id}")
def delete_fertilizer(fertilizer_id: int, db: Session = Depends(get_db)):
    deleted = fertilizer_crud.delete_fertilizer(db, fertilizer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Fertilizer not found")
    return {"message": f"🗑️ Fertilizer with id {fertilizer_id} deleted successfully"}
