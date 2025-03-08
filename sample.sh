

curl -i -X GET \
  "https://graph.instagram.com/v22.0/{instagram-account-id}/insights?metric=reach&period=day&breakdown=media_product_type&metric_type=total_value&since=1685991600&until=1686077999&access_token={your-access-token}"

# Likes, comments, shares, saved
curl -i -X GET \
  "https://graph.instagram.com/v22.0/{instagram-account-id}/insights?metric=likes,comments,shares,saved&period=day&metric_type=total_value&breakdown=media_product_type&access_token={your-access-token}"

# Audience demographics
curl -i -X GET \
  "https://graph.instagram.com/v22.0/{instagram-account-id}/insights?metric=audience_demographics&period=lifetime&timeframe=last_90_days&metric_type=total_value&access_token={your-access-token}"

# New views
curl -i -X GET \
  "https://graph.instagram.com/v22.0/{instagram-account-id}/insights?metric=views&period=day&breakdown=follower_type&metric_type=total_value&since=1685991600&until=1686077999&access_token={your-access-token}"

# Profile views
curl -i -X GET \
  "https://graph.instagram.com/v22.0/{instagram-account-id}/insights?metric=profile_views,website_clicks&period=day&metric_type=time_series&since=1685991600&until=1686077999&access_token={your-access-token}"