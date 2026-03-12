from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# ✅ Local imports
from app.database import Base, engine
from app.routers import (
    seed_router,
    fertilizer_router,
    crop_router,
    auth_router,
    product_router,
    live_rates_router,
    order_router,   # ✅ Keep this
)

# ✅ Create all DB tables (PostgreSQL)
Base.metadata.create_all(bind=engine)

# ✅ Initialize FastAPI
app = FastAPI(title="🌾 AgroMart API")

# ---------------------------------------------------------------
# 🧠 CORS SETUP (allows both local and production frontends)
# ---------------------------------------------------------------
allowed_origins = [
    "http://localhost:3000",          # Local Next.js frontend
    "https://agromart.in",            # Production domain
    "https://www.agromart.in",
    "https://agromart-frontend.vercel.app",  # Vercel deploy
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------
# 🖼️ Serve uploaded images & static files
# ---------------------------------------------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ---------------------------------------------------------------
# 🚜 Include all routers
# ---------------------------------------------------------------
app.include_router(seed_router.router, prefix="/api/seeds", tags=["Seeds"])
app.include_router(fertilizer_router.router, prefix="/api/fertilizers", tags=["Fertilizers"])
app.include_router(crop_router.router, prefix="/api/crops", tags=["Crops"])
app.include_router(auth_router.router, prefix="/api/auth", tags=["Auth"])
app.include_router(product_router.router, prefix="/api/products", tags=["Products"])
app.include_router(live_rates_router.router, prefix="/api/live-rates", tags=["Live Rates"])
app.include_router(order_router.router, prefix="/api/orders", tags=["Orders"])



# ---------------------------------------------------------------
# 🌾 Root health check
# ---------------------------------------------------------------
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "🌾 AgroMart Backend is running successfully with automatic live rate updates!",
        "frontend": "✅ CORS enabled for localhost and production domains",
    }
