from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class DataType(str, Enum):
    """
    Enum for different types of Instagram data
    """
    PROFILE = "profile"
    MEDIA = "media"
    MEDIA_INSIGHTS = "media_insights"
    USER_INSIGHTS = "user_insights"
    HASHTAG_MEDIA = "hashtag_media"


class AggregationStatus(BaseModel):
    """
    Schema for aggregation status
    """
    status: str = Field(..., description="Status of the aggregation process (success or error)")
    error: Optional[str] = Field(None, description="Error message if status is error")


class MediaInsightStatus(BaseModel):
    """
    Schema for media insight status
    """
    media_id: str = Field(..., description="ID of the media")
    status: str = Field(..., description="Status of the insights fetch (success or error)")
    error: Optional[str] = Field(None, description="Error message if status is error")


class HashtagStatus(BaseModel):
    """
    Schema for hashtag status
    """
    hashtag: str = Field(..., description="Hashtag name")
    count: Optional[int] = Field(None, description="Number of media items fetched")
    status: str = Field(..., description="Status of the hashtag fetch (success or error)")
    error: Optional[str] = Field(None, description="Error message if status is error")


class ProfileStatus(BaseModel):
    """
    Schema for profile status
    """
    username: Optional[str] = Field(None, description="Instagram username")
    status: str = Field(..., description="Status of the profile fetch (success or error)")
    error: Optional[str] = Field(None, description="Error message if status is error")


class MediaStatus(BaseModel):
    """
    Schema for media status
    """
    count: int = Field(..., description="Number of media items fetched")
    status: str = Field(..., description="Status of the media fetch (success or error)")
    error: Optional[str] = Field(None, description="Error message if status is error")


class MediaInsightsStatus(BaseModel):
    """
    Schema for media insights status
    """
    count: int = Field(..., description="Number of media insights fetched")
    items: List[MediaInsightStatus] = Field(..., description="Status for each media insight")


class HashtagsStatus(BaseModel):
    """
    Schema for hashtags status
    """
    count: int = Field(..., description="Number of hashtags processed")
    items: List[HashtagStatus] = Field(..., description="Status for each hashtag")


class AggregationSummary(BaseModel):
    """
    Schema for aggregation summary
    """
    profile: ProfileStatus = Field(..., description="Status of profile aggregation")
    media: MediaStatus = Field(..., description="Status of media aggregation")
    media_insights: Optional[MediaInsightsStatus] = Field(None, description="Status of media insights aggregation")
    user_insights: Optional[AggregationStatus] = Field(None, description="Status of user insights aggregation")
    hashtags: Optional[HashtagsStatus] = Field(None, description="Status of hashtags aggregation")


class DataAggregationRequest(BaseModel):
    """
    Schema for data aggregation request
    """
    media_limit: Optional[int] = Field(25, description="Maximum number of media items to fetch")
    hashtags: Optional[List[str]] = Field(None, description="List of hashtags to fetch media for")


class DataTypeRequest(BaseModel):
    """
    Schema for data type request
    """
    data_type: DataType = Field(..., description="Type of data to fetch")
    limit: Optional[int] = Field(25, description="Maximum number of items to fetch")
    hashtag: Optional[str] = Field(None, description="Hashtag name (only for HASHTAG_MEDIA type)")
    media_id: Optional[str] = Field(None, description="Media ID (only for MEDIA_INSIGHTS type)") 