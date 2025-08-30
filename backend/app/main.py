# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import get_database
from pymongo.errors import ConnectionFailure

# Import routers
from app.api import contracts
from app.routes import contract_routes
from app.routes import scoring_routes   # ✅ NEW scoring + gap analysis router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Contract Intelligence API for parsing, scoring, and managing contracts"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(
    contracts.router,
    prefix=f"{settings.API_V1_STR}/contracts",
    tags=["contracts"],
)

# Parsing routes
app.include_router(
    contract_routes.router,
    prefix=f"{settings.API_V1_STR}/contracts",
    tags=["parsing"]
)

# ✅ Scoring + Gap Analysis routes
app.include_router(
    scoring_routes.router,
    prefix=f"{settings.API_V1_STR}/scoring",
    tags=["scoring"]
)

# Health check root
@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

# Test DB connection on startup
@app.on_event("startup")
def startup_db_client():
    try:
        db = get_database()
        db.command("ping")  # MongoDB ping command
        print("✅ MongoDB connection successful")
    except ConnectionFailure as e:
        print(f"❌ MongoDB connection failed: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected MongoDB error: {e}")

@app.on_event("shutdown")
def shutdown_db_client():
    print("👋 Shutting down API")