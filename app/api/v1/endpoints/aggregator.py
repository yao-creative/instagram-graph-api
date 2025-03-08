from fastapi import APIRouter, Depends, Query, HTTPException, status, Body
from typing import Dict, List, Any, Optional
from pydantic.typing import Annotate

from app.schemas.aggregator import (
    DataAggregationRequest, AggregationSummary, DataType, DataTypeRequest
)
from app.schemas.responses import APIResponse
from app.services.data_aggregator import instagram_data_aggregator


# Create router
router = APIRouter()


@router.post(
    "/aggregate",
    response_model=APIResponse[AggregationSummary],
    summary="Aggregate Instagram Data",
    description="Fetches and stores Instagram data in Supabase"
)
async def aggregate_data(
    request: Annotate[DataAggregationRequest, Body(
        ...,
        examples=[{
            "media_limit": 25,
            "hashtags": ["travel", "food", "nature"]
        }]
    )]
):
    """
    Aggregate Instagram data and store it in Supabase.
    
    This endpoint fetches user profile, media, media insights, user insights,
    and optionally hashtag media data from Instagram Graph API and stores it in Supabase.
    
    **Example use cases:**
    - Daily/weekly data collection from Instagram
    - Archiving Instagram account data for analytics
    - Collecting hashtag data for social media research
    
    Returns a summary of the aggregation process.
    """
    try:
        result = await instagram_data_aggregator.aggregate_all_data(
            media_limit=request.media_limit,
            hashtags=request.hashtags
        )
        
        return {
            "status": "success",
            "message": "Data aggregation completed successfully",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during data aggregation: {str(e)}"
        )


@router.get(
    "/profile",
    response_model=APIResponse,
    summary="Get User Profile",
    description="Fetches user profile data from Instagram and stores it in Supabase"
)
async def get_profile():
    """
    Fetch user profile data from Instagram Graph API and store it in Supabase.
    
    Returns the profile data.
    """
    try:
        result = await instagram_data_aggregator.fetch_and_store_profile()
        
        return {
            "status": "success",
            "message": "Profile data fetched and stored successfully",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profile data: {str(e)}"
        )


@router.get(
    "/media",
    response_model=APIResponse,
    summary="Get User Media",
    description="Fetches user media data from Instagram and stores it in Supabase"
)
async def get_media(
    limit: Annotate[int, Query(25, description="Maximum number of media items to fetch")]
):
    """
    Fetch user media data from Instagram Graph API and store it in Supabase.
    
    Returns the media data.
    """
    try:
        result = await instagram_data_aggregator.fetch_and_store_media(limit=limit)
        
        return {
            "status": "success",
            "message": f"Fetched and stored {len(result)} media items",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching media data: {str(e)}"
        )


@router.get(
    "/media/{media_id}/insights",
    response_model=APIResponse,
    summary="Get Media Insights",
    description="Fetches insights for a specific media from Instagram and stores it in Supabase"
)
async def get_media_insights(
    media_id: str
):
    """
    Fetch insights for a specific media from Instagram Graph API and store it in Supabase.
    
    Returns the media insights data.
    """
    try:
        result = await instagram_data_aggregator.fetch_and_store_media_insights(media_id)
        
        return {
            "status": "success",
            "message": f"Fetched and stored insights for media {media_id}",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching media insights: {str(e)}"
        )


@router.get(
    "/user/insights",
    response_model=APIResponse,
    summary="Get User Insights",
    description="Fetches user insights from Instagram and stores it in Supabase"
)
async def get_user_insights():
    """
    Fetch user insights from Instagram Graph API and store it in Supabase.
    
    Returns the user insights data.
    """
    try:
        result = await instagram_data_aggregator.fetch_and_store_user_insights()
        
        return {
            "status": "success",
            "message": "Fetched and stored user insights",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user insights: {str(e)}"
        )


@router.get(
    "/hashtag/{hashtag_name}/media",
    response_model=APIResponse,
    summary="Get Hashtag Media",
    description="Fetches media with a specific hashtag from Instagram and stores it in Supabase"
)
async def get_hashtag_media(
    hashtag_name: str,
    limit: Annotate[int, Query(25, description="Maximum number of media items to fetch")]
):
    """
    Fetch media with a specific hashtag from Instagram Graph API and store it in Supabase.
    
    Returns the hashtag media data.
    """
    try:
        result = await instagram_data_aggregator.fetch_and_store_hashtag_media(
            hashtag_name=hashtag_name,
            limit=limit
        )
        
        return {
            "status": "success",
            "message": f"Fetched and stored {len(result)} media items for hashtag #{hashtag_name}",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching hashtag media: {str(e)}"
        ) 