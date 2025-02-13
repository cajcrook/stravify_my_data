import os
from flask import Flask, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
TOKEN_URL = "https://www.strava.com/oauth/token"

app = Flask(__name__)

def get_access_token():
    """Fetch a new access token using the refresh token."""
    response = requests.post(TOKEN_URL, data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,  # Correct usage
        "grant_type": "refresh_token"
    })
    data = response.json()
    print(data)  # Debugging

    if response.status_code != 200:
        return None  # Return None if refresh fails

    return data.get("access_token")

def get_activities():
    """Fetch activities from Strava API."""
    access_token = get_access_token()
    if not access_token:
        return {"error": "Failed to authenticate with Strava"}

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch activities", "status_code": response.status_code}

    return response.json()




@app.route('/', methods=['GET'])
def get_index():
    """Return activities as JSON in the browser."""
    return jsonify(get_activities())


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
