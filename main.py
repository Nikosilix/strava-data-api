from flask import Flask, jsonify
import requests

app = Flask(__name__)

ACCESS_TOKEN = "b600122189c2d0233095fa0eff77f198c35854ed"  # Your Strava access token

@app.route('/')
def home():
    return "✅ Strava Data Server is Running."

@app.route('/data')
def get_strava_data():
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"per_page": 30, "page": 1}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return {"error": "Failed to fetch activities"}, 500

    return jsonify(response.json())

app.run(host="0.0.0.0", port=81)