import httpx
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from app.models import (
    Metric, Period, MetricType, Breakdown, Timeframe,
    InsightsRequest, InstagramResponse, ApiResponse
)
from app.config import settings

class InstagramGraphService:
    """Service for interacting with the Instagram Graph API."""
    
    def __init__(self, access_token: Optional[str] = None):
        """Initialize the service with an access token."""
        self.access_token = access_token or settings.INSTAGRAM_ACCESS_TOKEN
        if not self.access_token:
            raise ValueError("Instagram access token is required")
        
        self.base_url = settings.INSTAGRAM_API_BASE_URL
        self.api_version = settings.INSTAGRAM_API_VERSION
    
    async def get_insights(self, request: InsightsRequest) -> ApiResponse:
        """Get insights from Instagram Graph API."""
        # Validate parameters based on metric type
        demographic_metrics = [
            Metric.AUDIENCE_DEMOGRAPHICS,
            Metric.ENGAGED_AUDIENCE_DEMOGRAPHICS,
            Metric.FOLLOWER_DEMOGRAPHICS
        ]
        
        if any(m in demographic_metrics for m in request.metrics) and not request.timeframe:
            raise ValueError("Timeframe is required for demographic metrics")
        
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
        
        if request.until:
            params["until"] = request.until
        
        # Make request to Instagram Graph API
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/{self.api_version}/{request.instagram_account_id}/insights"
            response = await client.get(url, params=params)
            
            # Handle errors
            if response.status_code != 200:
                error_data = response.json() if response.content else {"error": "Unknown error"}
                return ApiResponse(
                    status="error",
                    message=f"Instagram API error: {response.status_code}",
                    data=error_data
                )
            
            # Parse response
            instagram_response = response.json()
            return ApiResponse(
                status="success",
                data=instagram_response
            )
    
    def generate_sample_requests(self) -> Dict[str, Dict[str, str]]:
        """Generate sample requests for Instagram Graph API insights."""
        # Get current timestamp and timestamp for one year ago (from tomorrow)
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        one_year_ago = tomorrow - timedelta(days=365)
        since = int(one_year_ago.timestamp())
        until = int(now.timestamp())
        
        account_id = "{instagram-account-id}"
        
        samples = {
            "reach_with_breakdown": {
                "url": f"/api/v1/insights?instagram_account_id={account_id}&metrics=reach&period=day&metric_type=total_value&breakdowns=media_product_type&since={since}&until={until}",
                "description": "Get reach metrics with media product type breakdown (default one year of data)"
            },
            "interaction_metrics": {
                "url": f"/api/v1/insights?instagram_account_id={account_id}&metrics=likes&metrics=comments&metrics=shares&metrics=saved&period=day&metric_type=total_value&breakdowns=media_product_type&since={since}&until={until}",
                "description": "Get interaction metrics with media product type breakdown (default one year of data)"
            },
            "demographic_insights": {
                "url": f"/api/v1/insights?instagram_account_id={account_id}&metrics=audience_demographics&period=lifetime&timeframe=last_90_days&metric_type=total_value",
                "description": "Get audience demographic insights for the last 90 days"
            },
            "views_by_follower_type": {
                "url": f"/api/v1/insights?instagram_account_id={account_id}&metrics=views&period=day&breakdowns=follower_type&metric_type=total_value&since={since}&until={until}",
                "description": "Get views metrics broken down by follower type"
            },
            "profile_activity": {
                "url": f"/api/v1/insights?instagram_account_id={account_id}&metrics=profile_views&metrics=website_clicks&period=day&metric_type=time_series&since={since}&until={until}",
                "description": "Get profile activity metrics as a time series"
            },
            "follower_count": {
                "url": f"/api/v1/insights?instagram_account_id={account_id}&metrics=follower_count&period=day&metric_type=total_value",
                "description": "Get follower count"
            },
            "online_followers": {
                "url": f"/api/v1/insights?instagram_account_id={account_id}&metrics=online_followers&period=lifetime&metric_type=total_value",
                "description": "Get when your followers are online"
            }
        }
        
        return samples 