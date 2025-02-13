import os
from flask import Flask, jsonify, render_template
import requests
from dotenv import load_dotenv
from flask_cors import CORS


# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
TOKEN_URL = "https://www.strava.com/oauth/token"

app = Flask(__name__)
CORS(app) 


"""Fetch a new access token using the refresh token."""
def get_access_token():
    response = requests.post(TOKEN_URL, data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,  # Correct usage
        "grant_type": "refresh_token"
    })
    data = response.json()
    # print(data)  # Debugging
    if response.status_code != 200:
        return None  # Return None if refresh fails
    return data.get("access_token")



def get_all_activities():
    """Fetch activities from Strava API."""
    access_token = get_access_token()
    if not access_token:
        return {"error": "Failed to authenticate with Strava"}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch activities", "status_code": response.status_code}
    return response.json()



# Code for the 5 latest activity
def get_latest_10_activity():
    """Fetch the latest Strava activity."""
    activities = get_all_activities()
    if "error" in activities:
        return activities  # Return the error if authentication fails
    if isinstance(activities, list) and len(activities) > 0:
        return activities[:5]  # Return 10 latest activities
    return {"error": "No activities found"}




# # # Route for home
@app.route('/', methods=['GET'])
def get_index():
    """Return activities as JSON in the browser."""
    return render_template('index.html')

# # # Route for all activities
@app.route('/all', methods=['GET'])
def get_all():
    """Return activities as JSON in the browser."""
    return jsonify(get_all_activities())

# # # Route for lastest 10 activities
@app.route('/latest', methods=['GET'])
def latest_activity():
    """API route to fetch the latest activity."""
    return jsonify(get_latest_10_activity())  # Return only the latest activity

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
