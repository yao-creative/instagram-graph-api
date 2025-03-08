# Instagram Graph API Service

A FastAPI service for fetching Instagram insights using the Instagram Graph API v22.0.

## Features

- Fetch various Instagram insights metrics
- Support for breakdowns by media type, follower type, etc.
- Sample request generator
- Docker containerization with uv for package management
- Comprehensive API documentation
- Proper separation of concerns with layered architecture

## Architecture

The service follows a layered architecture pattern:

- **Routes Layer**: Handles HTTP requests/responses and parameter validation
- **Service Layer**: Contains business logic for interacting with the Instagram Graph API
- **Models Layer**: Defines data structures for requests and responses
- **Config Layer**: Manages configuration and environment variables

## Requirements

- Docker and Docker Compose
- Instagram Business or Creator account
- Instagram Graph API access token

## Setup

1. Clone this repository
2. Set your Instagram access token:

```bash
export INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token
```

3. Build and run the Docker container:

```bash
docker-compose up --build
```

4. Access the API documentation at http://localhost:8000/docs

## API Endpoints

### GET /api/v1/insights

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

### GET /api/v1/sample-requests

Get sample requests for Instagram Graph API insights.

### GET /api/v1/metrics

Get information about available metrics.

### GET /api/v1/breakdowns

Get information about available breakdowns.

## Available Metrics

### Interaction Metrics

- `accounts_engaged`: Number of accounts that have interacted with your content
- `comments`: Number of comments on your posts
- `follows`: Number of follows
- `likes`: Number of likes on your posts
- `profile_views`: Number of profile views
- `reach`: Number of unique accounts that have seen your content
- `replies`: Number of replies to your stories
- `saved`: Number of saves of your posts
- `shares`: Number of shares of your posts
- `total_interactions`: Total number of interactions
- `views`: Number of times your content was played or displayed
- `website_clicks`: Number of clicks on the website link in your profile

### Demographic Metrics

- `audience_demographics`: Demographic characteristics of your audience
- `engaged_audience_demographics`: Demographic characteristics of engaged audience
- `follower_demographics`: Demographic characteristics of your followers
- `online_followers`: When your followers are online
- `follower_count`: Number of followers

## Development

To run the application locally without Docker:

1. Install dependencies:

```bash
pip install uv
uv pip install -r requirements.txt
```

2. Run the application:

```bash
cd instagram-graph-api
uvicorn app.main:app --reload
```

## Project Structure

```
instagram-graph-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration settings
│   ├── models.py        # Data models
│   ├── routes.py        # API routes
│   └── services.py      # Business logic
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
``` 