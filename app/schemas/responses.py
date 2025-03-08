from typing import Optional, Dict, Any, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

# Define a type variable for generic response data
DataT = TypeVar("DataT")

class BaseResponse(BaseModel):
    """Base response model with status and message."""
    status: str
    message: Optional[str] = None

class APIResponse(GenericModel, Generic[DataT]):
    """Generic API response model for success responses."""
    status: str = "success"
    message: Optional[str] = None
    data: Optional[DataT] = None

class ErrorResponse(BaseResponse):
    """Error response model."""
    status: str = "error"
    message: str
    details: Optional[Dict[str, Any]] = None

class PagingData(BaseModel):
    """Pagination data model."""
    previous: Optional[str] = None
    next: Optional[str] = None 