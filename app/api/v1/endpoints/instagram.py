from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List, Optional, Any
from datetime import datetime, timedelta

from app.schemas.instagram import (
    Metric, Period, MetricType, Breakdown, Timeframe,
    InsightsRequest, SampleRequestsResponse
)
from app.schemas.responses import APIResponse
from app.services.instagram import InstagramGraphService, get_instagram_service

# Create router
router = APIRouter()


@router.get(
    "/insights",
    response_model=APIResponse,
    summary="Get Instagram Insights",
    description="Fetch insights from Instagram Graph API v22.0"
)
async def get_insights(
    instagram_account_id: str = Query(..., description="Instagram account ID"),
    metrics: List[Metric] = Query(..., description="List of metrics to fetch"),
    period: Period = Query(..., description="Period aggregation"),
    metric_type: MetricType = Query(..., description="How to aggregate results"),
    breakdowns: Optional[List[Breakdown]] = Query(None, description="How to break down result set"),
    timeframe: Optional[Timeframe] = Query(None, description="How far to look back for data (required for demographics)"),
    since: Optional[int] = Query(
        None, 
        description="Unix timestamp indicating start of range (default: one year ago)"
    ),
    until: Optional[int] = Query(
        None, 
        description="Unix timestamp indicating end of range (default: current time)"
    ),
    access_token: Optional[str] = Query(None, description="Instagram access token (if not provided, uses environment variable)"),
    service: InstagramGraphService = Depends(get_instagram_service)
):
    """
    Fetch insights from Instagram Graph API.
    
    This endpoint allows you to query various metrics from the Instagram Graph API v22.0
    with different aggregation periods and breakdowns.
    
    **Example use cases:**
    - Get account reach and engagement over time
    - Get follower demographics
    - Analyze content performance by media type
    """
    # Construct request object
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
    
    # Call service
    return await service.get_insights(request)


@router.get(
    "/sample-requests",
    response_model=SampleRequestsResponse,
    summary="Get Sample API Requests",
    description="Returns sample API requests that can be used as examples"
)
async def get_sample_requests(
    service: InstagramGraphService = Depends(get_instagram_service)
):
    """
    Get sample API requests for the Instagram Graph API.
    
    This endpoint provides example API requests that demonstrate
    common use cases for the Instagram Graph API endpoints.
    """
    samples = service.generate_sample_requests()
    return SampleRequestsResponse(samples=samples)


@router.get(
    "/metrics",
    summary="Get Available Metrics Information",
    description="Returns information about available metrics"
)
async def get_metrics_info():
    """
    Get information about available metrics.
    
    Returns detailed information about all available metrics that can be queried
    through the Instagram Graph API, including descriptions and requirements.
    """
    metrics_info = {
        "interaction_metrics": {
            "accounts_engaged": {
                "description": "Number of unique accounts that engaged with your content",
                "requirements": "Available for day and lifetime periods"
            },
            "comments": {
                "description": "Number of comments on your content",
                "requirements": "Available for day and lifetime periods"
            },
            "follows": {
                "description": "Number of follows of your account",
                "requirements": "Available for day and lifetime periods"
            },
            "likes": {
                "description": "Number of likes on your content",
                "requirements": "Available for day and lifetime periods"
            },
            "profile_views": {
                "description": "Number of views of your profile",
                "requirements": "Available for day and lifetime periods"
            },
            "reach": {
                "description": "Number of unique accounts that saw your content",
                "requirements": "Available for day and lifetime periods"
            },
            "replies": {
                "description": "Number of replies to your stories",
                "requirements": "Available for day and lifetime periods"
            },
            "saved": {
                "description": "Number of saves of your content",
                "requirements": "Available for day and lifetime periods"
            },
            "shares": {
                "description": "Number of shares of your content",
                "requirements": "Available for day and lifetime periods"
            },
            "total_interactions": {
                "description": "Total number of interactions on your content",
                "requirements": "Available for day and lifetime periods"
            },
            "views": {
                "description": "Number of views on your content (video)",
                "requirements": "Available for day and lifetime periods"
            },
            "website_clicks": {
                "description": "Number of clicks on your website link",
                "requirements": "Available for day and lifetime periods"
            }
        },
        "demographic_metrics": {
            "audience_demographics": {
                "description": "Demographic breakdown of your audience",
                "requirements": "Requires timeframe parameter"
            },
            "engaged_audience_demographics": {
                "description": "Demographic breakdown of accounts that engaged with your content",
                "requirements": "Requires timeframe parameter"
            },
            "follower_demographics": {
                "description": "Demographic breakdown of your followers",
                "requirements": "Requires timeframe parameter"
            },
            "online_followers": {
                "description": "Number of your followers online over time",
                "requirements": "Available for day period only"
            },
            "follower_count": {
                "description": "Total number of followers",
                "requirements": "Available for lifetime period only"
            }
        }
    }
    
    return APIResponse(
        status="success",
        data=metrics_info,
        message="Available metrics information"
    )


@router.get(
    "/breakdowns",
    summary="Get Available Breakdowns Information",
    description="Returns information about available breakdown dimensions"
)
async def get_breakdowns_info():
    """
    Get information about available breakdown dimensions.
    
    Returns detailed information about all available breakdown dimensions
    that can be used to segment Instagram Graph API data.
    """
    breakdowns_info = {
        "contact_button_type": {
            "description": "Breaks down insights by type of contact button clicked",
            "values": [
                "call_phone_number",
                "text_message",
                "email",
                "directions"
            ],
            "compatible_metrics": [
                "website_clicks"
            ]
        },
        "follow_type": {
            "description": "Breaks down follows by type",
            "values": [
                "follow",
                "unfollow"
            ],
            "compatible_metrics": [
                "follows"
            ]
        },
        "media_product_type": {
            "description": "Breaks down insights by media type",
            "values": [
                "feed",
                "story",
                "reels"
            ],
            "compatible_metrics": [
                "accounts_engaged",
                "comments",
                "likes",
                "reach",
                "saved",
                "shares",
                "total_interactions",
                "views"
            ]
        }
    }
    
    return APIResponse(
        status="success",
        data=breakdowns_info,
        message="Available breakdowns information"
    ) 