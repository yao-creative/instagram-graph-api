from fastapi import Request
import time
from loguru import logger
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests with performance metrics."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        logger.info(f"Request: {request_id} - {request.method} {request.url.path}")
        
        # Process the request and track timing
        start_time = time.time()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Extract status code
            status_code = response.status_code
            
            logger.info(
                f"Response: {request_id} - {request.method} {request.url.path} - "
                f"Status: {status_code} - Duration: {process_time:.4f}s"
            )
            
            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Error: {request_id} - {request.method} {request.url.path} - "
                f"Error: {str(e)} - Duration: {process_time:.4f}s"
            )
            raise 