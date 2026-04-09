"""
FULL DATABASE CREATION FILE
=====================================
Run this file ONCE to create all tables:

    python postgres_models.py

It will:
- Connect to PostgreSQL
- Create ALL tables
- Show them in PgAdmin immediately
"""

import sys
import os
import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Enum,
    ForeignKey,
    Integer,
    String,
    Float,
    Text,
    Boolean,
    DateTime,
    create_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
)

# Allow running directly: python postgres_models.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.db.config import DATABASE_URL

# ==========================================================
# DATABASE CONNECTION
# ==========================================================

engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass


# ==========================================================
# ENUMS
# ==========================================================

class UserRole(str, enum.Enum):
    BUYER  = "buyer"
    VENDOR = "vendor"

class ProductCategory(str, enum.Enum):
    CROP        = "Crop"
    SEED        = "Seed"
    FERTILIZER  = "Fertilizer"

class OrderStatus(str, enum.Enum):
    PENDING    = "Pending"
    CONFIRMED  = "Confirmed"
    SHIPPED    = "Shipped"
    DELIVERED  = "Delivered"
    CANCELLED  = "Cancelled"

class PaymentMethod(str, enum.Enum):
    BANK_TRANSFER    = "Bank Transfer"
    UPI              = "UPI"
    CASH_ON_DELIVERY = "Cash on Delivery"

class PaymentStatus(str, enum.Enum):
    PENDING  = "Pending"
    PAID     = "Paid"
    FAILED   = "Failed"
    REFUNDED = "Refunded"


# ==========================================================
# TABLE MODELS
# ==========================================================


# ----------------------------------------------------------
# USERS
# ----------------------------------------------------------

class Buyer(Base):
    __tablename__ = "buyers"

    id         : Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    name       : Mapped[str]           = mapped_column(String(100), nullable=False)
    email      : Mapped[str]           = mapped_column(String(255), unique=True, index=True, nullable=False)
    password   : Mapped[str]           = mapped_column(Text, nullable=False)
    is_active  : Mapped[bool]          = mapped_column(Boolean, default=True)
    created_at : Mapped[datetime]      = mapped_column(DateTime, default=datetime.utcnow)
    updated_at : Mapped[datetime]      = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Vendor(Base):
    __tablename__ = "vendors"

    id         : Mapped[int]           = mapped_column(Integer, primary_key=True, autoincrement=True)
    name       : Mapped[str]           = mapped_column(String(100), nullable=False)
    email      : Mapped[str]           = mapped_column(String(255), unique=True, index=True, nullable=False)
    password   : Mapped[str]           = mapped_column(Text, nullable=False)
    is_active  : Mapped[bool]          = mapped_column(Boolean, default=True)
    created_at : Mapped[datetime]      = mapped_column(DateTime, default=datetime.utcnow)
    updated_at : Mapped[datetime]      = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ----------------------------------------------------------
# PRODUCTS
# ----------------------------------------------------------

class Crop(Base):
    __tablename__ = "crops"

    id           : Mapped[int]            = mapped_column(Integer, primary_key=True, autoincrement=True)
    name         : Mapped[str]            = mapped_column(String(100), nullable=False)
    type         : Mapped[Optional[str]]  = mapped_column(String(50))
    price        : Mapped[Optional[float]]= mapped_column(Float)
    description  : Mapped[Optional[str]]  = mapped_column(Text)
    image_url    : Mapped[Optional[str]]  = mapped_column(Text)
    farmer_name  : Mapped[str]            = mapped_column(String(100), nullable=False)
    location     : Mapped[str]            = mapped_column(String(100), nullable=False)
    vendor_id    : Mapped[Optional[int]]  = mapped_column(Integer, ForeignKey("vendors.id", ondelete="SET NULL"))
    created_at   : Mapped[datetime]       = mapped_column(DateTime, default=datetime.utcnow)
    updated_at   : Mapped[datetime]       = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Seed(Base):
    __tablename__ = "seeds"

    id           : Mapped[int]            = mapped_column(Integer, primary_key=True, autoincrement=True)
    name         : Mapped[str]            = mapped_column(String(100), nullable=False)
    type         : Mapped[Optional[str]]  = mapped_column(String(50))
    price        : Mapped[Optional[float]]= mapped_column(Float)
    description  : Mapped[Optional[str]]  = mapped_column(Text)
    image_url    : Mapped[Optional[str]]  = mapped_column(Text)
    farmer_name  : Mapped[str]            = mapped_column(String(100), nullable=False)
    location     : Mapped[str]            = mapped_column(String(100), nullable=False)
    vendor_id    : Mapped[Optional[int]]  = mapped_column(Integer, ForeignKey("vendors.id", ondelete="SET NULL"))
    created_at   : Mapped[datetime]       = mapped_column(DateTime, default=datetime.utcnow)
    updated_at   : Mapped[datetime]       = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Fertilizer(Base):
    __tablename__ = "fertilizers"

    id           : Mapped[int]            = mapped_column(Integer, primary_key=True, autoincrement=True)
    name         : Mapped[str]            = mapped_column(String(100), nullable=False)
    type         : Mapped[Optional[str]]  = mapped_column(String(50))
    price        : Mapped[Optional[float]]= mapped_column(Float)
    description  : Mapped[Optional[str]]  = mapped_column(Text)
    image_url    : Mapped[Optional[str]]  = mapped_column(Text)
    farmer_name  : Mapped[str]            = mapped_column(String(100), nullable=False)
    location     : Mapped[str]            = mapped_column(String(100), nullable=False)
    vendor_id    : Mapped[Optional[int]]  = mapped_column(Integer, ForeignKey("vendors.id", ondelete="SET NULL"))
    created_at   : Mapped[datetime]       = mapped_column(DateTime, default=datetime.utcnow)
    updated_at   : Mapped[datetime]       = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"

    id          : Mapped[int]            = mapped_column(Integer, primary_key=True, autoincrement=True)
    name        : Mapped[str]            = mapped_column(String(100), nullable=False)
    price       : Mapped[float]          = mapped_column(Float, nullable=False)
    description : Mapped[Optional[str]]  = mapped_column(Text)
    category    : Mapped[Optional[str]]  = mapped_column(String(50))
    quantity    : Mapped[int]            = mapped_column(Integer, default=0)
    vendor_id   : Mapped[int]            = mapped_column(Integer, ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False)
    created_at  : Mapped[datetime]       = mapped_column(DateTime, default=datetime.utcnow)
    updated_at  : Mapped[datetime]       = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ----------------------------------------------------------
# ORDERS
# ----------------------------------------------------------

class Order(Base):
    __tablename__ = "orders"

    id             : Mapped[int]            = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_uuid     : Mapped[str]            = mapped_column(String(100), unique=True, nullable=False)
    buyer_id       : Mapped[Optional[int]]  = mapped_column(Integer, ForeignKey("buyers.id", ondelete="SET NULL"))
    buyer_name     : Mapped[Optional[str]]  = mapped_column(String(100))
    total_price    : Mapped[float]          = mapped_column(Float, nullable=False)
    currency       : Mapped[str]            = mapped_column(String(10), default="INR")
    status         : Mapped[str]            = mapped_column(
                                                Enum(OrderStatus, values_callable=lambda x: [e.value for e in x]),
                                                default=OrderStatus.PENDING.value
                                             )
    payment_method : Mapped[Optional[str]]  = mapped_column(
                                                Enum(PaymentMethod, values_callable=lambda x: [e.value for e in x])
                                             )
    payment_status : Mapped[str]            = mapped_column(
                                                Enum(PaymentStatus, values_callable=lambda x: [e.value for e in x]),
                                                default=PaymentStatus.PENDING.value
                                             )
    source_ip      : Mapped[Optional[str]]  = mapped_column(String(50))
    created_at     : Mapped[datetime]       = mapped_column(DateTime, default=datetime.utcnow)
    updated_at     : Mapped[datetime]       = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OrderItem(Base):
    __tablename__ = "order_items"

    id         : Mapped[int]   = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id   : Mapped[int]   = mapped_column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id : Mapped[str]   = mapped_column(String(100), nullable=False)
    name       : Mapped[str]   = mapped_column(String(100), nullable=False)
    quantity   : Mapped[int]   = mapped_column(Integer, nullable=False)
    price      : Mapped[float] = mapped_column(Float, nullable=False)


# ==========================================================
# RUN DIRECTLY — creates all tables in PgAdmin
# ==========================================================

if __name__ == "__main__":
    print("Connecting to:", DATABASE_URL)
    try:
        Base.metadata.create_all(engine)
        print("\n✅ PostgreSQL schema created successfully!")
        print("✅ Tables created:")
        for table in Base.metadata.tables:
            print(f"   - {table}")
    except Exception as e:
        print("❌ Schema creation failed:", e)
        sys.exit(1)
