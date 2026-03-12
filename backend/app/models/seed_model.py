from sqlalchemy import Column, Integer, String, Float, Text
from app.database import Base

class Seed(Base):
    __tablename__ = "seeds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=True)
    price = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    farmer_name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
