from fastapi import APIRouter
from app.api.v1.endpoints import instagram, aggregator

# Create API v1 router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(instagram.router, prefix="/instagram", tags=["Instagram"])
api_router.include_router(aggregator.router, prefix="/aggregator", tags=["Data Aggregator"])

# Add more routers as needed
# api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"]) 