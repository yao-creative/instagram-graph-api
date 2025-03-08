import asyncio
from typing import Dict, List, Any
from datetime import datetime
import json
from loguru import logger

from app.core.config import settings
from app.db.supabase import supabase_client
from app.services.instagram_api import instagram_api


class InstagramDataAggregator:
    """
    Service for aggregating Instagram data and storing it in Supabase
    """
    
    def __init__(self):
        self.instagram_api = instagram_api
        self.supabase_client = supabase_client
        self.table_name = settings.SUPABASE_TABLE_NAME
        
    async def fetch_and_store_profile(self) -> Dict[str, Any]:
        """
        Fetch user profile data and store it in Supabase
        
        Returns:
            Profile data
        """
        try:
            logger.info("Fetching user profile data")
            profile_data = self.instagram_api.get_user_profile()
            
            # Add timestamp
            profile_data["fetched_at"] = datetime.utcnow().isoformat()
            profile_data["data_type"] = "profile"
            
            # Store in Supabase
            await self.supabase_client.upsert_data(
                self.table_name,
                profile_data,
                on_conflict="id"
            )
            
            logger.info(f"Stored profile data for user {profile_data.get('username')}")
            return profile_data
        except Exception as e:
            logger.error(f"Error fetching and storing profile data: {e}")
            raise
            
    async def fetch_and_store_media(self, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Fetch user media data and store it in Supabase
        
        Args:
            limit: Maximum number of media to fetch
            
        Returns:
            List of media data
        """
        try:
            logger.info(f"Fetching up to {limit} media items")
            media_list = self.instagram_api.get_user_media(limit=limit)
            
            stored_media = []
            for media in media_list:
                # Add timestamp and data type
                media["fetched_at"] = datetime.utcnow().isoformat()
                media["data_type"] = "media"
                
                # Handle nested data (children)
                if "children" in media and isinstance(media["children"], dict):
                    media["children"] = json.dumps(media["children"])
                
                # Store in Supabase
                await self.supabase_client.upsert_data(
                    self.table_name,
                    media,
                    on_conflict="id"
                )
                
                stored_media.append(media)
                
            logger.info(f"Stored {len(stored_media)} media items")
            return stored_media
        except Exception as e:
            logger.error(f"Error fetching and storing media data: {e}")
            raise
            
    async def fetch_and_store_media_insights(self, media_id: str) -> Dict[str, Any]:
        """
        Fetch insights for a specific media and store in Supabase
        
        Args:
            media_id: ID of the media
            
        Returns:
            Media insights data
        """
        try:
            logger.info(f"Fetching insights for media {media_id}")
            insights_data = self.instagram_api.get_media_insights(media_id)
            
            # Add metadata
            insights_data["media_id"] = media_id
            insights_data["fetched_at"] = datetime.utcnow().isoformat()
            insights_data["data_type"] = "media_insights"
            
            # Convert insights data to a proper format for storage
            if "data" in insights_data and isinstance(insights_data["data"], list):
                formatted_insights = {"id": f"{media_id}_insights"}
                
                for metric in insights_data["data"]:
                    metric_name = metric.get("name")
                    metric_value = metric.get("values", [{}])[0].get("value")
                    if metric_name and metric_value is not None:
                        formatted_insights[metric_name] = metric_value
                
                formatted_insights["fetched_at"] = insights_data["fetched_at"]
                formatted_insights["data_type"] = insights_data["data_type"]
                
                # Store in Supabase
                await self.supabase_client.upsert_data(
                    self.table_name,
                    formatted_insights,
                    on_conflict="id"
                )
                
                logger.info(f"Stored insights for media {media_id}")
                return formatted_insights
            else:
                logger.warning(f"No valid insights data found for media {media_id}")
                return insights_data
        except Exception as e:
            logger.error(f"Error fetching and storing media insights: {e}")
            raise
            
    async def fetch_and_store_user_insights(self) -> Dict[str, Any]:
        """
        Fetch user insights and store in Supabase
        
        Returns:
            User insights data
        """
        try:
            logger.info("Fetching user insights")
            insights_data = self.instagram_api.get_user_insights()
            
            # Get user ID from profile
            profile_data = self.instagram_api.get_user_profile()
            user_id = profile_data.get("id")
            
            if not user_id:
                raise ValueError("Could not get user ID from profile")
                
            # Add metadata
            insights_data["user_id"] = user_id
            insights_data["fetched_at"] = datetime.utcnow().isoformat()
            insights_data["data_type"] = "user_insights"
            insights_data["id"] = f"{user_id}_insights"
            
            # Convert insights data structure for storage
            if "data" in insights_data and isinstance(insights_data["data"], list):
                formatted_insights = {"id": insights_data["id"]}
                
                for metric in insights_data["data"]:
                    metric_name = metric.get("name")
                    # Handle different metric value structures
                    if "values" in metric:
                        values = metric.get("values", [{}])[0]
                        if "value" in values:
                            formatted_insights[metric_name] = values["value"]
                        elif isinstance(values, dict):
                            # For complex metrics like audience_gender_age
                            formatted_insights[metric_name] = json.dumps(values)
                
                formatted_insights["user_id"] = insights_data["user_id"]
                formatted_insights["fetched_at"] = insights_data["fetched_at"]
                formatted_insights["data_type"] = insights_data["data_type"]
                
                # Store in Supabase
                await self.supabase_client.upsert_data(
                    self.table_name,
                    formatted_insights,
                    on_conflict="id"
                )
                
                logger.info(f"Stored user insights for user {user_id}")
                return formatted_insights
            else:
                logger.warning("No valid user insights data found")
                return insights_data
        except Exception as e:
            logger.error(f"Error fetching and storing user insights: {e}")
            raise
            
    async def fetch_and_store_hashtag_media(self, hashtag_name: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Fetch media with a specific hashtag and store in Supabase
        
        Args:
            hashtag_name: Name of the hashtag without the # symbol
            limit: Maximum number of media to fetch
            
        Returns:
            List of hashtag media data
        """
        try:
            logger.info(f"Fetching hashtag media for #{hashtag_name}")
            
            # Get hashtag ID
            hashtag_id = self.instagram_api.get_hashtag_id(hashtag_name)
            
            # Get hashtag media
            media_list = self.instagram_api.get_hashtag_media(hashtag_id, limit=limit)
            
            stored_media = []
            for media in media_list:
                # Add metadata
                media["hashtag"] = hashtag_name
                media["hashtag_id"] = hashtag_id
                media["fetched_at"] = datetime.utcnow().isoformat()
                media["data_type"] = "hashtag_media"
                
                # Store in Supabase
                await self.supabase_client.upsert_data(
                    self.table_name,
                    media,
                    on_conflict="id"
                )
                
                stored_media.append(media)
                
            logger.info(f"Stored {len(stored_media)} media items for hashtag #{hashtag_name}")
            return stored_media
        except Exception as e:
            logger.error(f"Error fetching and storing hashtag media: {e}")
            raise
            
    async def aggregate_all_data(self, media_limit: int = 25, hashtags: List[str] = None) -> Dict[str, Any]:
        """
        Aggregate all Instagram data and store in Supabase
        
        Args:
            media_limit: Maximum number of media to fetch
            hashtags: List of hashtags to fetch media for
            
        Returns:
            Summary of aggregated data
        """
        summary = {}
        
        try:
            # Fetch and store profile
            profile = await self.fetch_and_store_profile()
            summary["profile"] = {"username": profile.get("username"), "status": "success"}
            
            # Fetch and store media
            media_list = await self.fetch_and_store_media(limit=media_limit)
            summary["media"] = {"count": len(media_list), "status": "success"}
            
            # Fetch and store media insights for each media
            media_insights = []
            for media in media_list:
                try:
                    media_id = media.get("id")
                    if media_id:
                        insights = await self.fetch_and_store_media_insights(media_id)
                        media_insights.append({"media_id": media_id, "status": "success"})
                except Exception as e:
                    logger.error(f"Error processing media insights for {media.get('id')}: {e}")
                    media_insights.append({"media_id": media.get("id"), "status": "error", "error": str(e)})
                    
            summary["media_insights"] = {"count": len(media_insights), "items": media_insights}
            
            # Fetch and store user insights
            try:
                user_insights = await self.fetch_and_store_user_insights()
                summary["user_insights"] = {"status": "success"}
            except Exception as e:
                logger.error(f"Error processing user insights: {e}")
                summary["user_insights"] = {"status": "error", "error": str(e)}
                
            # Fetch and store hashtag media
            if hashtags:
                hashtag_results = []
                for hashtag in hashtags:
                    try:
                        hashtag_media = await self.fetch_and_store_hashtag_media(hashtag, limit=media_limit)
                        hashtag_results.append({
                            "hashtag": hashtag,
                            "count": len(hashtag_media),
                            "status": "success"
                        })
                    except Exception as e:
                        logger.error(f"Error processing hashtag {hashtag}: {e}")
                        hashtag_results.append({
                            "hashtag": hashtag,
                            "status": "error",
                            "error": str(e)
                        })
                        
                summary["hashtags"] = {"count": len(hashtag_results), "items": hashtag_results}
                
            logger.info("Completed data aggregation")
            return summary
        except Exception as e:
            logger.error(f"Error in data aggregation: {e}")
            raise


# Create singleton instance
instagram_data_aggregator = InstagramDataAggregator() 