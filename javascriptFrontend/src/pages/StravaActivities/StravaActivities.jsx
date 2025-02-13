import { useState } from "react";
import './StravaActivities.css'; 

const StravaActivities = () => {
    const [activities, setActivities] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const loadActivities = async () => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch("http://localhost:5001/latest"); 
            const data = await response.json();

            if (data.error) {
                setError(data.error);
                setActivities([]);
            } else {
                setActivities(data);
            }
        } catch (err) {
            setError("Failed to load activities");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="activities-container">
            <h1 className="title">Latest Strava Activities</h1>
            <button
                onClick={loadActivities}
                className="load-button"
            >
                Load Activities
            </button>

            {loading && <p className="loading-text">Loading...</p>}
            {error && <p className="error-text">{error}</p>}

            <div className="activities-list">
                {activities.map((activity) => (
                    <div key={activity.id} className="activity">
                        <strong>{activity.name}</strong>
                        <p>Distance: {(activity.distance / 1000).toFixed(2)} km</p>
                        <p>Duration: {(activity.moving_time / 60).toFixed(1)} min</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default StravaActivities;
