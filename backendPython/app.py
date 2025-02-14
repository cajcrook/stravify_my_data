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


#   Fetch a new access token using the refresh token.
def get_access_token():
    response = requests.post(TOKEN_URL, data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,  
        "grant_type": "refresh_token"
    })
    data = response.json()
    # print(data)  # Debugging
    if response.status_code != 200:
        return None  # Return None if refresh fails
    return data.get("access_token")



#   Fetch activities from Strava API.
def get_all_activities():
    access_token = get_access_token()
    if not access_token:
        return {"error": "Failed to authenticate with Strava"}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch activities", "status_code": response.status_code}
    return response.json()


#   Fetch the latest Strava activity.
def get_latest_5_activity():
    activities = get_all_activities()
    if "error" in activities:
        return activities  # Return the error if authentication fails
    if isinstance(activities, list) and len(activities) > 0:
        return activities[:5]  # Return 5 latest activities
    return {"error": "No activities found"}


#   Fetch the latest Strava activity filtered by sport.
def get_latest_5_activity_by_sport(sport_type):
    activities = get_all_activities()
    if "error" in activities:
        return activities  # Return the error if authentication fails
    filtered_activities = [activity for activity in activities if activity['sport_type'].lower() == sport_type.lower()]
    return filtered_activities[:5] if filtered_activities else {"error": "No activities found for this sport."}



#   Route for home
@app.route('/', methods=['GET'])
def get_index():
    """Return activities as JSON in the browser."""
    return render_template('index.html')

#   Route for all activities
@app.route('/all', methods=['GET'])
def get_all():
    """Return activities as JSON in the browser."""
    return jsonify(get_all_activities())

#   Route for lastest 5 activities
@app.route('/latest', methods=['GET'])
def latest_activity():
    return jsonify(get_latest_5_activity())  # Return only the latest activity

#   Route for latest activities by sport
@app.route('/latest/<sport>', methods=['GET'])
def latest_activity_by_sport(sport):
    """API route to fetch the latest activities by selected sport."""
    return jsonify(get_latest_5_activity_by_sport(sport))  # Return only the latest 5 activities for the selected sport


#  Return overall stats for all activities.
@app.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    activities = get_all_activities()
    if "error" in activities:
        return jsonify(activities)

    total_distance = sum(a["distance"] for a in activities) / 1000  # Convert meters to km
    total_time = sum(a["moving_time"] for a in activities) / 3600  # Convert seconds to hours
    total_elevation = sum(a["total_elevation_gain"] for a in activities)

    return jsonify({
        "total_distance_km": round(total_distance, 2),
        "total_time_hours": round(total_time, 2),
        "total_elevation_m": round(total_elevation, 2),
        "total_activities": len(activities)
    })


#  Return stats for the last 7 days.
@app.route('/dashboard/weekly', methods=['GET'])
def get_weekly_stats():
    from datetime import datetime, timedelta
    activities = get_all_activities()
    if "error" in activities:
        return jsonify(activities)

    one_week_ago = datetime.now() - timedelta(days=7)
    weekly_activities = [a for a in activities if datetime.strptime(a["start_date"], "%Y-%m-%dT%H:%M:%SZ") > one_week_ago]

    total_distance = sum(a["distance"] for a in weekly_activities) / 1000
    total_time = sum(a["moving_time"] for a in weekly_activities) / 3600
    total_elevation = sum(a["total_elevation_gain"] for a in weekly_activities)

    return jsonify({
        "weekly_distance_km": round(total_distance, 2),
        "weekly_time_hours": round(total_time, 2),
        "weekly_elevation_m": round(total_elevation, 2),
        "weekly_activities": len(weekly_activities)
    })

#   Return stats for the last 30 days.
@app.route('/dashboard/monthly', methods=['GET'])
def get_monthly_stats():
    from datetime import datetime, timedelta
    activities = get_all_activities()
    if "error" in activities:
        return jsonify(activities)

    one_month_ago = datetime.now() - timedelta(days=30)
    monthly_activities = [a for a in activities if datetime.strptime(a["start_date"], "%Y-%m-%dT%H:%M:%SZ") > one_month_ago]

    total_distance = sum(a["distance"] for a in monthly_activities) / 1000
    total_time = sum(a["moving_time"] for a in monthly_activities) / 3600
    total_elevation = sum(a["total_elevation_gain"] for a in monthly_activities)

    return jsonify({
        "monthly_distance_km": round(total_distance, 2),
        "monthly_time_hours": round(total_time, 2),
        "monthly_elevation_m": round(total_elevation, 2),
        "monthly_activities": len(monthly_activities)
    })


#   Return best performance metrics from activities.
@app.route('/dashboard/personal_bests', methods=['GET'])
def get_personal_bests():
    activities = get_all_activities()
    if "error" in activities:
        return jsonify(activities)

    longest_ride = max(activities, key=lambda a: a["distance"], default=None)
    fastest_run = min((a for a in activities if a["sport_type"].lower() == "run"), key=lambda a: a["elapsed_time"] / a["distance"], default=None)

    return jsonify({
        "longest_ride_km": round(longest_ride["distance"] / 1000, 2) if longest_ride else None,
        "fastest_run_pace_min_per_km": round((fastest_run["elapsed_time"] / 60) / (fastest_run["distance"] / 1000), 2) if fastest_run else None
    })


#   Return stats for a specific sport (run, ride, swim).
@app.route('/dashboard/sport_summary/<sport>', methods=['GET'])
def get_sport_summary(sport):
    activities = get_all_activities()
    if "error" in activities:
        return jsonify(activities)

    filtered_activities = [a for a in activities if a["sport_type"].lower() == sport.lower()]
    if not filtered_activities:
        return jsonify({"error": f"No activities found for sport: {sport}"})

    total_distance = sum(a["distance"] for a in filtered_activities) / 1000
    total_time = sum(a["moving_time"] for a in filtered_activities) / 3600
    total_elevation = sum(a["total_elevation_gain"] for a in filtered_activities)

    return jsonify({
        f"{sport}_distance_km": round(total_distance, 2),
        f"{sport}_time_hours": round(total_time, 2),
        f"{sport}_elevation_m": round(total_elevation, 2),
        f"{sport}_activities": len(filtered_activities)
    })




if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))