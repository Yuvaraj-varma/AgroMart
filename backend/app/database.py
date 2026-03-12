from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Create SQLAlchemy engine (echo=True helps debug DB logs, optional)
engine = create_engine(DATABASE_URL, echo=True)

# ✅ Create session for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for models
Base = declarative_base()

# ✅ Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
