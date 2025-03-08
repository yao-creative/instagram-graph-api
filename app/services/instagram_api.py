import requests
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings


class InstagramGraphAPI:
    """
    Client for interacting with Instagram Graph API
    """
    
    def __init__(self):
        self.base_url = settings.INSTAGRAM_API_BASE_URL
        self.api_version = settings.INSTAGRAM_API_VERSION
        self.access_token = settings.INSTAGRAM_ACCESS_TOKEN
        
        if not self.access_token:
            logger.error("Instagram access token not provided")
            raise ValueError("Instagram access token is required")
            
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the Instagram Graph API
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            API response as dictionary
        """
        if params is None:
            params = {}
            
        # Add access token to parameters
        params["access_token"] = self.access_token
        
        # Construct full URL
        url = urljoin(f"{self.base_url}/{self.api_version}/", endpoint)
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error occurred: {e}")
            raise
        except ValueError:
            logger.error("Invalid JSON response")
            raise
            
    def get_user_profile(self) -> Dict[str, Any]:
        """
        Get the user profile information
        
        Returns:
            User profile data
        """
        endpoint = "me"
        fields = "id,username,account_type,media_count"
        
        return self._make_request(endpoint, {"fields": fields})
        
    def get_user_media(self, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Get user's media
        
        Args:
            limit: Maximum number of media to return
            
        Returns:
            List of media data
        """
        endpoint = "me/media"
        fields = "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username,children{media_url}"
        
        response = self._make_request(endpoint, {"fields": fields, "limit": limit})
        
        media_list = []
        if "data" in response:
            media_list = response["data"]
            
            # Handle pagination
            while "paging" in response and "next" in response["paging"] and len(media_list) < limit:
                try:
                    response = requests.get(response["paging"]["next"]).json()
                    if "data" in response:
                        media_list.extend(response["data"])
                except Exception as e:
                    logger.error(f"Error fetching paginated media: {e}")
                    break
                    
        return media_list[:limit]
        
    def get_media_insights(self, media_id: str) -> Dict[str, Any]:
        """
        Get insights for a specific media
        
        Args:
            media_id: ID of the media
            
        Returns:
            Media insights data
        """
        endpoint = f"{media_id}/insights"
        metric = "engagement,impressions,reach,saved"
        
        return self._make_request(endpoint, {"metric": metric})
        
    def get_user_insights(self) -> Dict[str, Any]:
        """
        Get insights for the user account
        
        Returns:
            User insights data
        """
        endpoint = "me/insights"
        metric = "audience_gender_age,audience_locale,audience_country,online_followers"
        period = "lifetime"
        
        return self._make_request(endpoint, {"metric": metric, "period": period})
        
    def get_hashtag_id(self, hashtag_name: str) -> str:
        """
        Get the ID of a hashtag
        
        Args:
            hashtag_name: Name of the hashtag without the # symbol
            
        Returns:
            Hashtag ID
        """
        endpoint = "ig_hashtag_search"
        
        response = self._make_request(endpoint, {"q": hashtag_name})
        
        if "data" in response and response["data"]:
            return response["data"][0]["id"]
        else:
            logger.error(f"Hashtag {hashtag_name} not found")
            raise ValueError(f"Hashtag {hashtag_name} not found")
            
    def get_hashtag_media(self, hashtag_id: str, limit: int = 25) -> List[Dict[str, Any]]:
        """
        Get recent media with a specific hashtag
        
        Args:
            hashtag_id: ID of the hashtag
            limit: Maximum number of media to return
            
        Returns:
            List of media data
        """
        endpoint = f"{hashtag_id}/recent_media"
        fields = "id,caption,media_type,media_url,permalink,timestamp,username"
        
        response = self._make_request(endpoint, {"fields": fields, "limit": limit})
        
        media_list = []
        if "data" in response:
            media_list = response["data"]
            
            # Handle pagination
            while "paging" in response and "next" in response["paging"] and len(media_list) < limit:
                try:
                    response = requests.get(response["paging"]["next"]).json()
                    if "data" in response:
                        media_list.extend(response["data"])
                except Exception as e:
                    logger.error(f"Error fetching paginated hashtag media: {e}")
                    break
                    
        return media_list[:limit]


# Create singleton instance
instagram_api = InstagramGraphAPI() 