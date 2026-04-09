from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.db.config import DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError(
        "No PostgreSQL configuration found. Set DATABASE_URL in the .env file."
    )

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"Error in database operation: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    """
    Create PostgreSQL extensions (if possible) and all tables.
    Call this once during FastAPI startup.
    """
    # Import models so their metadata is populated
    try:
        import app.db.postgres_models as models  # noqa: F401
    except Exception as e:
        print(f"Could not import postgres_models: {e}")
        raise

    # Try to enable useful extensions (idempotent)
    try:
        with engine.connect() as conn:
            conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
            conn.commit()
    except Exception:
        # Extensions may require superuser — ignore and proceed
        pass

    # Create all tables from models metadata
    try:
        models.Base.metadata.create_all(bind=engine)
        print("✅ PostgreSQL tables created successfully.")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise
