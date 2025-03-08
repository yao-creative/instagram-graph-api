from supabase import create_client
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger

from app.core.config import settings

class SupabaseClient:
    """
    Supabase client for handling connection and database operations
    """
    
    def __init__(self):
        self.client = self._initialize_client()
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def _initialize_client(self):
        """Initialize Supabase client with retry logic"""
        try:
            logger.info("Initializing Supabase client")
            return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise
            
    async def insert_data(self, table_name: str, data: dict):
        """
        Insert data into Supabase table
        
        Args:
            table_name: Name of the table to insert data into
            data: Dictionary containing data to insert
            
        Returns:
            Response from Supabase
        """
        try:
            response = self.client.table(table_name).insert(data).execute()
            return response
        except Exception as e:
            logger.error(f"Failed to insert data into {table_name}: {e}")
            raise
            
    async def upsert_data(self, table_name: str, data: dict, on_conflict: str):
        """
        Upsert data into Supabase table
        
        Args:
            table_name: Name of the table to upsert data into
            data: Dictionary containing data to upsert
            on_conflict: Column to check for conflicts
            
        Returns:
            Response from Supabase
        """
        try:
            response = self.client.table(table_name).upsert(data, on_conflict=on_conflict).execute()
            return response
        except Exception as e:
            logger.error(f"Failed to upsert data into {table_name}: {e}")
            raise
            
    async def select_data(self, table_name: str, columns: str = "*", query_params: dict = None):
        """
        Select data from Supabase table
        
        Args:
            table_name: Name of the table to select data from
            columns: Columns to select
            query_params: Dictionary containing query parameters
            
        Returns:
            Response from Supabase
        """
        try:
            query = self.client.table(table_name).select(columns)
            
            if query_params:
                for key, value in query_params.items():
                    query = query.eq(key, value)
                    
            response = query.execute()
            return response
        except Exception as e:
            logger.error(f"Failed to select data from {table_name}: {e}")
            raise

# Create a singleton instance
supabase_client = SupabaseClient() 