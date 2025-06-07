from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

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

    try:
        data = response.json()
        if not isinstance(data, list):
            return {"error": "Unexpected data format"}, 500

        activities = sorted(
            [a for a in data if a.get("type") == "Run" and "start_date_local" in a],
            key=lambda x: x["start_date_local"],
            reverse=True
        )
        return jsonify(activities)
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/exchange_token')
def exchange_token():
    code = request.args.get('code')
    if not code:
        return "Missing code", 400

    payload = {
        'client_id': 163386,
        'client_secret': '70e5f82ea9729fc4c54ca6f13880d917054478c5',
        'code': code,
        'grant_type': 'authorization_code'
    }

    response = requests.post('https://www.strava.com/oauth/token', data=payload)
    return response.json()