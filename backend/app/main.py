from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.postgres_session import create_tables
from app.db.mongo_session import create_collections
from app.routers import (
    seed_router,
    fertilizer_router,
    crop_router,
    auth_router,
    product_router,
    live_rates_router,
    order_router,
    vendor_router,
)

# ✅ Create all DB tables on startup
create_tables()
create_collections()

# ✅ Initialize FastAPI
app = FastAPI(title="🌾 AgroMart API")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve uploaded images
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(settings.UPLOAD_DIR)), name="uploads")

# ✅ Routers
app.include_router(seed_router.router,        prefix="/api/seeds",       tags=["Seeds"])
app.include_router(fertilizer_router.router,  prefix="/api/fertilizers", tags=["Fertilizers"])
app.include_router(crop_router.router,        prefix="/api/crops",       tags=["Crops"])
app.include_router(auth_router.router,        prefix="/api/auth",        tags=["Auth"])
app.include_router(product_router.router,     prefix="/api/products",    tags=["Products"])
app.include_router(live_rates_router.router,  prefix="/api/live-rates",  tags=["Live Rates"])
app.include_router(order_router.router,       prefix="/api/orders",      tags=["Orders"])
app.include_router(vendor_router.router,       prefix="/api/vendor",      tags=["Vendor Dashboard"])


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "🌾 AgroMart Backend is running!",
        "docs": "/docs",
    }
