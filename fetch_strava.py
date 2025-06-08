import requests
import json
import time

# Replace with your real client credentials
CLIENT_ID = "163386"
CLIENT_SECRET = "70e5f82ea9729fc4c54ca6f13880d917054478c5"

# Read stored token data
with open("token.json", "r") as f:
    token_data = json.load(f)

# Check expiration
if token_data["expires_at"] < time.time():
    print("🔄 Token expired. Refreshing...")
    response = requests.post(
        "https://www.strava.com/api/v3/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": token_data["refresh_token"]
        }
    )
    if response.status_code != 200:
        print("❌ Failed to refresh token:", response.text)
        exit(1)

    token_data = response.json()
    with open("token.json", "w") as f:
        json.dump(token_data, f)
else:
    print("✅ Token still valid.")

# Fetch activities
headers = {"Authorization": f"Bearer {token_data['access_token']}"}
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
    print("❌ Failed to fetch data:", response.text)