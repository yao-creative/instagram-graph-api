from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.middleware.logging_middleware import RequestLoggingMiddleware
from app.middleware.error_handler import http_error_handler, APIException, api_exception_handler

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A service for fetching Instagram insights using the Instagram Graph API v22.0",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Add exception handlers
app.add_exception_handler(Exception, http_error_handler)
app.add_exception_handler(APIException, api_exception_handler)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that provides basic information about the API.
    """
    return {
        "message": f"{settings.PROJECT_NAME} is running",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "api_prefix": settings.API_V1_PREFIX,
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring systems.
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 