-- Create Instagram data table
CREATE TABLE IF NOT EXISTS instagram_data (
    id TEXT PRIMARY KEY,
    username TEXT,
    account_type TEXT,
    media_count INTEGER,
    caption TEXT,
    media_type TEXT,
    media_url TEXT,
    permalink TEXT,
    thumbnail_url TEXT,
    timestamp TIMESTAMP,
    children JSONB,
    engagement INTEGER,
    impressions INTEGER,
    reach INTEGER,
    saved INTEGER,
    audience_gender_age JSONB,
    audience_locale JSONB,
    audience_country JSONB,
    online_followers JSONB,
    hashtag TEXT,
    hashtag_id TEXT,
    user_id TEXT,
    media_id TEXT,
    data_type TEXT NOT NULL,
    fetched_at TIMESTAMP NOT NULL
);

-- Create index on data_type for faster querying
CREATE INDEX IF NOT EXISTS idx_instagram_data_data_type ON instagram_data(data_type);

-- Create index on fetched_at for time-based queries
CREATE INDEX IF NOT EXISTS idx_instagram_data_fetched_at ON instagram_data(fetched_at);

-- Create index on username for user-based queries
CREATE INDEX IF NOT EXISTS idx_instagram_data_username ON instagram_data(username);

-- Create index on hashtag for hashtag-based queries
CREATE INDEX IF NOT EXISTS idx_instagram_data_hashtag ON instagram_data(hashtag); 