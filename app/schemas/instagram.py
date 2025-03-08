from enum import Enum
from typing import List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

# Enums for parameter validation
class Period(str, Enum):
    DAY = "day"
    WEEK = "week"
    LIFETIME = "lifetime"

class MetricType(str, Enum):
    TOTAL_VALUE = "total_value"
    TIME_SERIES = "time_series"

class Timeframe(str, Enum):
    LAST_7_DAYS = "last_7_days"
    LAST_14_DAYS = "last_14_days"
    LAST_30_DAYS = "last_30_days"
    LAST_90_DAYS = "last_90_days"

class Breakdown(str, Enum):
    CONTACT_BUTTON_TYPE = "contact_button_type"
    FOLLOW_TYPE = "follow_type"
    MEDIA_PRODUCT_TYPE = "media_product_type"

class Metric(str, Enum):
    # Interaction Metrics
    ACCOUNTS_ENGAGED = "accounts_engaged"
    COMMENTS = "comments"
    FOLLOWS = "follows"
    LIKES = "likes"
    PROFILE_VIEWS = "profile_views"
    REACH = "reach"
    REPLIES = "replies"
    SAVED = "saved"
    SHARES = "shares"
    TOTAL_INTERACTIONS = "total_interactions"
    VIEWS = "views"
    WEBSITE_CLICKS = "website_clicks"
    
    # Demographic Metrics
    AUDIENCE_DEMOGRAPHICS = "audience_demographics"
    ENGAGED_AUDIENCE_DEMOGRAPHICS = "engaged_audience_demographics"
    FOLLOWER_DEMOGRAPHICS = "follower_demographics"
    ONLINE_FOLLOWERS = "online_followers"
    FOLLOWER_COUNT = "follower_count"

# Request Models
class InsightsRequest(BaseModel):
    """Request model for Instagram insights."""
    instagram_account_id: str = Field(..., description="Instagram account ID")
    metrics: List[Metric] = Field(..., description="List of metrics to fetch")
    period: Period = Field(..., description="Period aggregation")
    metric_type: MetricType = Field(..., description="How to aggregate results")
    breakdowns: Optional[List[Breakdown]] = Field(None, description="How to break down result set")
    timeframe: Optional[Timeframe] = Field(None, description="How far to look back for data")
    since: Optional[int] = Field(
        None, 
        description="Unix timestamp indicating start of range. Defaults to one year ago from tomorrow if not provided."
    )
    until: Optional[int] = Field(
        None, 
        description="Unix timestamp indicating end of range. Defaults to current timestamp if not provided."
    )
    access_token: Optional[str] = Field(None, description="Instagram access token")

# Response models
class BreakdownResult(BaseModel):
    dimension_values: List[str]
    value: int
    end_time: Optional[str] = None

class BreakdownData(BaseModel):
    dimension_keys: List[str]
    results: List[BreakdownResult]

class TotalValue(BaseModel):
    value: Optional[int] = None
    breakdowns: Optional[List[BreakdownData]] = None

class TimeSeriesValue(BaseModel):
    value: int
    end_time: str

class MetricData(BaseModel):
    name: str
    period: str
    title: str
    description: str
    total_value: Optional[TotalValue] = None
    values: Optional[List[TimeSeriesValue]] = None
    id: str

class InstagramResponse(BaseModel):
    data: List[MetricData]
    paging: Optional[Any] = None

# Sample request models
class SampleRequest(BaseModel):
    """Sample request model."""
    url: str
    description: str

class SampleRequestsResponse(BaseModel):
    """Sample requests response model."""
    samples: dict[str, SampleRequest] 