# Instagram Graph API Service

A production-ready FastAPI service for fetching Instagram insights using the Instagram Graph API v22.0.

## Features

- Fetch various Instagram insights metrics
- Support for breakdowns by media type, follower type, etc.
- Sample request generator
- Docker containerization
- Modern dependency management with pyproject.toml and uv
- Comprehensive API documentation
- Proper separation of concerns with layered architecture
- Advanced logging with Loguru
- Standardized error handling
- Type-safe configuration with Pydantic
- Comprehensive test suite
- **Instagram Data Aggregator with Supabase storage**

## Architecture

The service follows a clean architecture pattern:

- **API Layer**: Handles HTTP requests/responses and parameter validation
- **Service Layer**: Contains business logic for interacting with the Instagram Graph API
- **Schemas Layer**: Defines data structures for requests and responses
- **Core Layer**: Manages configuration, logging, and other core functionality
- **Middleware Layer**: Handles cross-cutting concerns like logging and error handling
- **Utils Layer**: Provides utility functions for common tasks

## Data Aggregator

The Instagram Data Aggregator component provides functionality to fetch data from Instagram Graph API and store it in a Supabase database. This is useful for:

- Archiving Instagram data for historical analysis
- Building custom analytics dashboards
- Collecting Instagram content and hashtag data
- Backing up Instagram account data

### Data Types Collected

The aggregator collects and stores the following types of data:

- User Profile: Basic account information
- Media: Photos, videos, and albums posted by the user
- Media Insights: Engagement metrics for each media
- User Insights: Account-level insights including audience demographics
- Hashtag Media: Content from specified hashtags

### Supabase Integration

The service uses Supabase as a backend database to store the collected Instagram data. The aggregator:

1. Connects to Instagram Graph API
2. Fetches data from various endpoints
3. Processes the data into a suitable structure
4. Stores the processed data in Supabase for later retrieval and analysis

## Setup with Supabase

To use the data aggregator with a local Supabase instance:

1. Install Docker if you don't already have it installed
2. Run the setup script to initialize Supabase locally:

```bash
# Using the script defined in pyproject.toml
uv run setup-supabase

# Or directly
python setup_supabase.py
```

This script will:
- Check for required dependencies
- Install Supabase CLI if needed
- Initialize a Supabase project
- Create the necessary database schema
- Start Supabase and provide connection details
- Update your .env file with the Supabase URL and key

## Requirements

- Python 3.9+
- Instagram Business or Creator account
- Instagram Graph API access token

## Setup

1. Clone this repository
2. Create a `.env` file with your Instagram access token:

```bash
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token
```

3. Install dependencies using uv:

```bash
# Install uv if you don't have it
pip install uv

# Install project dependencies
uv pip install -e .

# For development dependencies
uv pip install -e ".[dev]"
```

4. Run the application:

```bash
# Using the script defined in pyproject.toml
uv run start

# Or directly
uv run uvicorn app.main:app --reload
```

5. Access the API documentation at http://localhost:8000/docs

## Docker Setup

1. Build and run the Docker container:

```bash
docker-compose up --build
```

2. Access the API documentation at http://localhost:8000/docs

## API Endpoints

### GET /api/v1/instagram/insights

Fetch insights from Instagram Graph API.

**Parameters:**

- `instagram_account_id` (required): Instagram account ID
- `metrics` (required): List of metrics to fetch
- `period` (required): Period aggregation (day, week, lifetime)
- `metric_type` (required): How to aggregate results (total_value, time_series)
- `breakdowns` (optional): How to break down result set
- `timeframe` (optional): How far to look back for data (required for demographics)
- `since` (optional): Unix timestamp indicating start of range
- `until` (optional): Unix timestamp indicating end of range
- `access_token` (optional): Instagram access token (if not provided, uses environment variable)

### GET /api/v1/instagram/sample-requests

Get sample requests for Instagram Graph API insights.

### GET /api/v1/instagram/metrics

Get information about available metrics.

### GET /api/v1/instagram/breakdowns

Get information about available breakdowns.

### Data Aggregator API

The data aggregator provides the following endpoints:

#### POST /api/v1/aggregator/aggregate

Aggregates all Instagram data and stores it in Supabase.

Example request:
```json
{
  "media_limit": 25,
  "hashtags": ["travel", "food", "nature"]
}
```

#### GET /api/v1/aggregator/profile

Fetches and stores user profile data.

#### GET /api/v1/aggregator/media

Fetches and stores media data.

#### GET /api/v1/aggregator/media/{media_id}/insights

Fetches and stores insights for a specific media.

#### GET /api/v1/aggregator/user/insights

Fetches and stores user insights including audience demographics.

#### GET /api/v1/aggregator/hashtag/{hashtag_name}/media

Fetches and stores media from a specific hashtag.

## Available Metrics

### Interaction Metrics

- `