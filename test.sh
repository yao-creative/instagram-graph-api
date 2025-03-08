curl -i -X GET "https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=acd09613baa87be91b24f58ec270b9d9&access_token=IGAAXbUbjZB0zpBZAE02THNQTHRYQkVKNWtvMGJrZAWIwV3VLakdfZAHZADeEhCXzhKbnFidWRsajVFbHRBcTVJRTBhRUJIN2hQNk01amJKS2NZASm9WZAi16UG11TWt6Yk9ZAUDFDd3ZAMM0ZAVREpRdEM3bGpTQlgzNW1hNkN4RGktUFNzNAZDZD"



GET "https://<HOST_URL>/<API_VERSION>/<INSTAGRAM_MEDIA_ID>/insights
  ?metric=<LIST_OF_METRICS>
  &period=<LIST_OF_TIME_PERIODS>
  &breakdown=<LIST_OF_BREAKDOWNS>
  &access_token=<ACCESS_TOKEN>"



curl -i -X GET "https://graph.instagram.com/v22.0/17841408199665394/insights?metric=impressions,reach,profile_views&period=day"


curl -X GET "https://graph.instagram.com/v22.0/17841408199665394/insights?metric=reach&period=day&access_token=IGAAXbUbjZB0zpBZAE02THNQTHRYQkVKNWtvMGJrZAWIwV3VLakdfZAHZADeEhCXzhKbnFidWRsajVFbHRBcTVJRTBhRUJIN2hQNk01amJKS2NZASm9WZAi16UG11TWt6Yk9ZAUDFDd3ZAMM0ZAVREpRdEM3bGpTQlgzNW1hNkN4RGktUFNzNAZDZD"


# 
curl -i -X GET \
  "https://graph.instagram.com/v22.0/17841408199665394/insights?metric=views&period=day&breakdown=follower_type&metric_type=total_value&since=1685991600&until=1686077999&access_token=IGAAXbUbjZB0zpBZAE02THNQTHRYQkVKNWtvMGJrZAWIwV3VLakdfZAHZADeEhCXzhKbnFidWRsajVFbHRBcTVJRTBhRUJIN2hQNk01amJKS2NZASm9WZAi16UG11TWt6Yk9ZAUDFDd3ZAMM0ZAVREpRdEM3bGpTQlgzNW1hNkN4RGktUFNzNAZDZD"

curl -i -X GET \
  "https://graph.instagram.com/v22.0/17841408199665394/insights?metric=likes,comments,shares,saved&period=day&metric_type=total_value&breakdown=media_product_type&access_token=IGAAXbUbjZB0zpBZAE02THNQTHRYQkVKNWtvMGJrZAWIwV3VLakdfZAHZADeEhCXzhKbnFidWRsajVFbHRBcTVJRTBhRUJIN2hQNk01amJKS2NZASm9WZAi16UG11TWt6Yk9ZAUDFDd3ZAMM0ZAVREpRdEM3bGpTQlgzNW1hNkN4RGktUFNzNAZDZD"