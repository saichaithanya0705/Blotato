from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path
import logging

# Import routes
from routes.auth import router as auth_router
from routes.content import router as content_router
from routes.analytics import router as analytics_router
from routes.public import router as public_router
from storage import init_storage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(title="Blotato Clone API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check route
@api_router.get("/")
async def root():
    return {"message": "Blotato Clone API is running!", "status": "healthy"}

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(content_router)
api_router.include_router(analytics_router)
api_router.include_router(public_router)

# Include the main router in the app
app.include_router(api_router)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_storage():
    """Initialize storage on startup."""
    await init_storage()
    logger.info("File storage initialized successfully")

@app.on_event("shutdown")
async def shutdown_storage():
    """Cleanup on shutdown."""
    logger.info("Shutting down file storage")