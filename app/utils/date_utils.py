from datetime import datetime, timedelta
from typing import Tuple


def get_default_date_range(days_back: int = 365) -> Tuple[int, int]:
    """
    Get default date range for API queries.
    
    Args:
        days_back (int): Number of days to look back from tomorrow.
        
    Returns:
        Tuple of (since, until) timestamps.
    """
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    since_date = tomorrow - timedelta(days=days_back)
    
    return int(since_date.timestamp()), int(now.timestamp())


def format_timestamp(timestamp: int) -> str:
    """
    Format a Unix timestamp into a human-readable date string.
    
    Args:
        timestamp (int): Unix timestamp.
        
    Returns:
        Formatted date string.
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def parse_date_string(date_str: str) -> int:
    """
    Parse a date string into a Unix timestamp.
    
    Args:
        date_str (str): Date string in YYYY-MM-DD format.
        
    Returns:
        Unix timestamp.
        
    Raises:
        ValueError: If date string format is invalid.
    """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return int(dt.timestamp())
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Expected YYYY-MM-DD.") 