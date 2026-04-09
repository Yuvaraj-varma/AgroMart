import pytest
from pydantic import ValidationError
from app.schemas.crop_schema import CropCreate
from app.schemas.seed_schema import SeedCreate
from app.schemas.fertilizer_schema import FertilizerCreate
from app.schemas.user import UserCreate


# ── Crop Validation ──────────────────────────────────────────
def test_crop_valid():
    crop = CropCreate(name="Rice", price=50.0, description="Fresh rice")
    assert crop.name == "Rice"


def test_crop_negative_price():
    with pytest.raises(ValidationError):
        CropCreate(name="Rice", price=-10)


def test_crop_zero_price():
    with pytest.raises(ValidationError):
        CropCreate(name="Rice", price=0)


def test_crop_short_name():
    with pytest.raises(ValidationError):
        CropCreate(name="R", price=50)


def test_crop_short_description():
    with pytest.raises(ValidationError):
        CropCreate(name="Rice", price=50, description="Hi")


# ── Seed Validation ──────────────────────────────────────────
def test_seed_valid():
    seed = SeedCreate(name="Wheat Seed", price=100.0, description="Certified wheat")
    assert seed.name == "Wheat Seed"


def test_seed_negative_price():
    with pytest.raises(ValidationError):
        SeedCreate(name="Wheat", price=-5)


# ── Fertilizer Validation ────────────────────────────────────
def test_fertilizer_valid():
    f = FertilizerCreate(name="Urea", price=200.0, description="Nitrogen fertilizer")
    assert f.name == "Urea"


def test_fertilizer_zero_price():
    with pytest.raises(ValidationError):
        FertilizerCreate(name="Urea", price=0)


# ── User Validation ──────────────────────────────────────────
def test_user_valid():
    user = UserCreate(name="Yuvaraj", email="yuvaraj@test.com", password="pass123", role="buyer")
    assert user.role == "buyer"


def test_user_short_password():
    with pytest.raises(ValidationError):
        UserCreate(name="Yuvaraj", email="y@test.com", password="123", role="buyer")


def test_user_invalid_role():
    with pytest.raises(ValidationError):
        UserCreate(name="Yuvaraj", email="y@test.com", password="pass123", role="admin")


def test_user_short_name():
    with pytest.raises(ValidationError):
        UserCreate(name="Y", email="y@test.com", password="pass123", role="buyer")
