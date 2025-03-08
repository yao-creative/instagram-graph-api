import httpx
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from loguru import logger
from fastapi import Depends, HTTPException, status

from app.schemas.instagram import (
    Metric, Period, MetricType, Breakdown, Timeframe,
    InsightsRequest, InstagramResponse, SampleRequest
)
from app.schemas.responses import APIResponse
from app.core.config import settings


class InstagramGraphService:
    """Service for interacting with the Instagram Graph API."""
    
    def __init__(self, access_token: Optional[str] = None):
        """Initialize the service with an access token."""
        self.access_token = access_token or settings.INSTAGRAM_ACCESS_TOKEN
        if not self.access_token:
            raise ValueError("Instagram access token is required")
        
        self.base_url = settings.INSTAGRAM_API_BASE_URL
        self.api_version = settings.INSTAGRAM_API_VERSION
        logger.debug(f"Instagram Graph Service initialized with API version {self.api_version}")
    
    async def get_insights(self, request: InsightsRequest) -> APIResponse:
        """
        Get insights from Instagram Graph API.
        
        Args:
            request: The insights request parameters.
            
        Returns:
            API response with Instagram insights data.
            
        Raises:
            HTTPException: If API request fails or parameters are invalid.
        """
        # Validate parameters based on metric type
        demographic_metrics = [
            Metric.AUDIENCE_DEMOGRAPHICS,
            Metric.ENGAGED_AUDIENCE_DEMOGRAPHICS,
            Metric.FOLLOWER_DEMOGRAPHICS
        ]
        
        if any(m in demographic_metrics for m in request.metrics) and not request.timeframe:
            logger.error("Timeframe is required for demographic metrics")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Timeframe is required for demographic metrics"
            )
        
        # Use provided token or instance token
        token = request.access_token or self.access_token
        
        # Build query parameters
        params = {
            "metric": ",".join([m.value for m in request.metrics]),
            "period": request.period.value,
            "metric_type": request.metric_type.value,
            "access_token": token
        }
        
        if request.breakdowns:
            params["breakdown"] = ",".join([b.value for b in request.breakdowns])
        
        if request.timeframe:
            params["timeframe"] = request.timeframe.value
        
        if request.since:
            params["since"] = request.since
        else:
            # Default to one year ago from tomorrow
            tomorrow = datetime.now() + timedelta(days=1)
            one_year_ago = tomorrow - timedelta(days=365)
            params["since"] = int(one_year_ago.timestamp())
        
        if request.until:
            params["until"] = request.until
        else:
            # Default to current time
            params["until"] = int(datetime.now().timestamp())
        
        # Build URL
        url = f"{self.base_url}/{self.api_version}/{request.instagram_account_id}/insights"
        
        try:
            logger.debug(f"Making request to Instagram API: {url} with params: {params}")
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                # Parse response
                instagram_response = InstagramResponse.parse_obj(response.json())
                
                return APIResponse(
                    status="success",
                    message="Successfully retrieved Instagram insights",
                    data=instagram_response
                )
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Instagram API error: {e.response.text}"
            )
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Error connecting to Instagram API: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )
    
    def generate_sample_requests(self) -> Dict[str, SampleRequest]:
        """
        Generate sample API requests for demonstration purposes.
        
        Returns:
            A dictionary of sample requests with descriptions.
        """
        base_url = f"/api/v1/insights?instagram_account_id=ACCOUNT_ID&access_token=YOUR_TOKEN"
        
        return {
            "reach_engagement_day": SampleRequest(
                url=f"{base_url}&metrics=reach,profile_views,accounts_engaged&period=day&metric_type=total_value",
                description="Get total reach, profile views, and engaged accounts for the day"
            ),
            "reach_engagement_time_series": SampleRequest(
                url=f"{base_url}&metrics=reach,profile_views,accounts_engaged&period=day&metric_type=time_series",
                description="Get time series data for reach, profile views, and engaged accounts"
            ),
            "follower_demographics": SampleRequest(
                url=f"{base_url}&metrics=follower_demographics&period=lifetime&metric_type=total_value&timeframe=last_30_days",
                description="Get follower demographics for the last 30 days"
            ),
            "content_interactions_with_breakdown": SampleRequest(
                url=f"{base_url}&metrics=likes,comments,shares&period=day&metric_type=total_value&breakdowns=media_product_type",
                description="Get content interactions broken down by media type"
            ),
            "audience_reach_breakdown": SampleRequest(
                url=f"{base_url}&metrics=reach,impressions&period=day&metric_type=total_value&breakdowns=age,gender,country",
                description="Get reach and impressions broken down by age, gender, and country"
            )
        }


def get_instagram_service(access_token: Optional[str] = None) -> InstagramGraphService:
    """
    Dependency function to get an Instagram Graph Service instance.
    
    Args:
        access_token: Optional access token to override the one in settings.
        
    Returns:
        An initialized InstagramGraphService instance.
        
    Raises:
        HTTPException: If service initialization fails.
    """
    try:
        return InstagramGraphService(access_token=access_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 