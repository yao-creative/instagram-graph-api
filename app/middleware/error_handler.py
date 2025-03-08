from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Union, Dict, Any
from loguru import logger

from app.schemas.responses import ErrorResponse


async def http_error_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Generic error handler for all exceptions.
    Returns a standardized error response with appropriate status code.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            status="error",
            message="An unexpected error occurred",
            details={"error": str(exc)}
        ).dict(),
    )


class APIException(Exception):
    """Base class for custom API exceptions with standardized error responses."""
    
    def __init__(
        self,
        status_code: int,
        message: str,
        details: Union[Dict[str, Any], None] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.details = details
        super().__init__(message)


async def api_exception_handler(_: Request, exc: APIException) -> JSONResponse:
    """
    Handler for custom API exceptions.
    Returns a standardized error response with the specified status code.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status="error",
            message=exc.message,
            details=exc.details
        ).dict(),
    ) 