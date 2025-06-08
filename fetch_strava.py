import os
import time
import requests
import json

# Load environment variables
ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
EXPIRES_AT = int(os.getenv("STRAVA_EXPIRES_AT", 0))
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

print("🧪 DEBUG - Loaded env vars:")
print("ACCESS_TOKEN:", ACCESS_TOKEN)
print("REFRESH_TOKEN:", REFRESH_TOKEN)
print("EXPIRES_AT:", EXPIRES_AT)
print("Current Time:", int(time.time()))

# Refresh the token if expired
if time.time() > EXPIRES_AT:
    print("🔄 Access token expired, refreshing...")

    res = requests.post(
        "https://www.strava.com/api/v3/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN
        }
    )

    if res.status_code != 200:
        print("❌ Failed to refresh token:", res.status_code, res.text)
        exit(1)

    new_token = res.json()
    ACCESS_TOKEN = new_token["access_token"]
    REFRESH_TOKEN = new_token["refresh_token"]
    EXPIRES_AT = new_token["expires_at"]

    print("✅ Token refreshed.")
    print("🔑 New Access Token:", ACCESS_TOKEN)
    print("⏳ New Expiry:", EXPIRES_AT)

else:
    print("✅ Token still valid.")

# Fetch activities
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
params = {"per_page": 30, "page": 1}

response = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=headers, params=params)

if response.status_code == 200:
    activities = sorted(
        [a for a in response.json() if a["type"] == "Run"],
        key=lambda x: x["start_date_local"],
        reverse=True
    )
    with open("cached_data.json", "w") as f:
        json.dump(activities, f, indent=2)
    print("✅ Data updated and saved to cached_data.json")
else:
    print("❌ Failed to fetch data:", response.status_code, response.text)