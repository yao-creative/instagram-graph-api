from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
import time

from app.models import (
    Metric, Period, MetricType, Breakdown, Timeframe,
    ApiResponse, SampleRequestsResponse, SampleRequest, InsightsRequest
)
from app.services import InstagramGraphService
from app.config import settings

# Create router
router = APIRouter(prefix=settings.API_V1_PREFIX)

# Dependency to get Instagram Graph Service
def get_instagram_service():
    try:
        return InstagramGraphService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights", response_model=ApiResponse, tags=["Insights"])
async def get_insights(
    instagram_account_id: str = Query(..., description="Instagram account ID"),
    metrics: List[Metric] = Query(..., description="List of metrics to fetch"),
    period: Period = Query(..., description="Period aggregation"),
    metric_type: MetricType = Query(..., description="How to aggregate results"),
    breakdowns: Optional[List[Breakdown]] = Query(None, description="How to break down result set"),
    timeframe: Optional[Timeframe] = Query(None, description="How far to look back for data (required for demographics)"),
    since: Optional[int] = Query(int((datetime.now() - timedelta(days=365)).timestamp()), description="Unix timestamp indicating start of range"),
    until: Optional[int] = Query(int(datetime.now().timestamp()), description="Unix timestamp indicating end of range"),
    access_token: Optional[str] = Query(None, description="Instagram access token (if not provided, uses environment variable)"),
    service: InstagramGraphService = Depends(get_instagram_service)
):
    """
    Fetch insights from Instagram Graph API.
    
    This endpoint allows you to query various metrics from the Instagram Graph API v22.0.
    """
    try:
        # Set default time range if not provided: one year ago (from tomorrow) to now
        now = datetime.now()
        if since is None:
            # Calculate one year ago from tomorrow
            tomorrow = now + timedelta(days=1)
            one_year_ago = tomorrow - timedelta(days=365)
            since = int(one_year_ago.timestamp())
        
        if until is None:
            until = int(now.timestamp())
            
        # Create request model
        request = InsightsRequest(
            instagram_account_id=instagram_account_id,
            metrics=metrics,
            period=period,
            metric_type=metric_type,
            breakdowns=breakdowns,
            timeframe=timeframe,
            since=since,
            until=until,
            access_token=access_token
        )
        
        # Get insights from service
        return await service.get_insights(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/sample-requests", response_model=SampleRequestsResponse, tags=["Samples"])
async def get_sample_requests(
    service: InstagramGraphService = Depends(get_instagram_service)
):
    """
    Get sample requests for Instagram Graph API insights.
    """
    try:
        samples_dict = service.generate_sample_requests()
        samples = {k: SampleRequest(**v) for k, v in samples_dict.items()}
        return SampleRequestsResponse(samples=samples)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Metric information endpoint
@router.get("/metrics", tags=["Metadata"])
async def get_metrics_info():
    """
    Get information about available metrics.
    """
    metrics_info = {
        # Interaction Metrics
        "accounts_engaged": {
            "description": "The number of accounts that have interacted with your content",
            "period": ["day"],
            "breakdowns": [],
            "metric_type": ["total_value"]
        },
        "comments": {
            "description": "The number of comments on your posts, reels, videos and live videos",
            "period": ["day"],
            "breakdowns": ["media_product_type"],
            "metric_type": ["total_value"]
        },
        "follows": {
            "description": "The number of new followers",
            "period": ["day"],
            "breakdowns": [],
            "metric_type": ["total_value"]
        },
        "likes": {
            "description": "The number of likes on your posts, reels, and videos",
            "period": ["day"],
            "breakdowns": ["media_product_type"],
            "metric_type": ["total_value"]
        },
        "profile_views": {
            "description": "The number of times your profile was viewed",
            "period": ["day"],
            "breakdowns": [],
            "metric_type": ["total_value", "time_series"]
        },
        "reach": {
            "description": "The number of unique accounts that have seen your content",
            "period": ["day"],
            "breakdowns": ["media_product_type", "follow_type"],
            "metric_type": ["total_value", "time_series"]
        },
        "replies": {
            "description": "The number of replies you received from your story",
            "period": ["day"],
            "breakdowns": [],
            "metric_type": ["total_value"]
        },
        "saved": {
            "description": "The number of saves of your posts, reels, and videos",
            "period": ["day"],
            "breakdowns": ["media_product_type"],
            "metric_type": ["total_value"]
        },
        "shares": {
            "description": "The number of shares of your posts, stories, reels, videos and live videos",
            "period": ["day"],
            "breakdowns": ["media_product_type"],
            "metric_type": ["total_value"]
        },
        "total_interactions": {
            "description": "The total number of interactions",
            "period": ["day"],
            "breakdowns": ["media_product_type"],
            "metric_type": ["total_value"]
        },
        "views": {
            "description": "The number of times your content was played or displayed",
            "period": ["day"],
            "breakdowns": ["follower_type", "media_product_type"],
            "metric_type": ["total_value"]
        },
        "website_clicks": {
            "description": "The number of clicks on the website link in your profile",
            "period": ["day"],
            "breakdowns": [],
            "metric_type": ["total_value", "time_series"]
        },
        
        # Demographic Metrics
        "audience_demographics": {
            "description": "Demographic characteristics of your audience",
            "period": ["lifetime"],
            "breakdowns": [],
            "metric_type": ["total_value"],
            "requires_timeframe": True
        },
        "engaged_audience_demographics": {
            "description": "Demographic characteristics of engaged audience",
            "period": ["lifetime"],
            "breakdowns": [],
            "metric_type": ["total_value"],
            "requires_timeframe": True
        },
        "follower_demographics": {
            "description": "Demographic characteristics of your followers",
            "period": ["lifetime"],
            "breakdowns": [],
            "metric_type": ["total_value"],
            "requires_timeframe": True
        },
        "online_followers": {
            "description": "When your followers are online",
            "period": ["lifetime"],
            "breakdowns": [],
            "metric_type": ["total_value"]
        },
        "follower_count": {
            "description": "Number of followers",
            "period": ["day", "lifetime"],
            "breakdowns": [],
            "metric_type": ["total_value", "time_series"]
        }
    }
    
    return {"metrics": metrics_info}

# Breakdown information endpoint
@router.get("/breakdowns", tags=["Metadata"])
async def get_breakdowns_info():
    """
    Get information about available breakdowns.
    """
    breakdowns_info = {
        "contact_button_type": {
            "description": "Break down results by profile UI component that viewers tapped or clicked",
            "values": ["BOOK_NOW", "CALL", "DIRECTION", "EMAIL", "INSTANT_EXPERIENCE", "TEXT", "UNDEFINED"]
        },
        "follow_type": {
            "description": "Break down results by followers or non-followers",
            "values": ["FOLLOWER", "NON_FOLLOWER", "UNKNOWN"]
        },
        "media_product_type": {
            "description": "Break down results by the surface where viewers viewed or interacted with the app user's media",
            "values": ["AD", "FEED", "REELS", "STORY"]
        }
    }
    
    return {"breakdowns": breakdowns_info} 