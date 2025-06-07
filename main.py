from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

ACCESS_TOKEN = "b600122189c2d0233095fa0eff77f198c35854ed"  # Your Strava access token

@app.route('/')
def home():
    return "✅ Strava Data Server is Running."

@app.route('/data')
def get_cached_data():
    try:
        with open("cached_data.json", "r") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return {"error": "Unexpected data format"}, 500

        activities = sorted(
            [a for a in data if a.get("type") == "Run" and "start_date_local" in a],
            key=lambda x: x["start_date_local"],
            reverse=True
        )
        return jsonify(activities)

    except Exception as e:
        return {"error": f"Failed to read local cache: {str(e)}"}, 500

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