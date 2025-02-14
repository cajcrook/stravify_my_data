import React from 'react';
import { Card, CardContent } from '../ui/Card';
import './PersonalBests.css';  

const PersonalBests = ({ personalBests }) => {
  return (
    <div>      
    <h2 className="subtitle">Personal Bests</h2>
    <div className="personal-bests-row">
      <div className="personal-bests-col">
        <Card>
          <CardContent>
            <h3 className="card-header">Longest Ride</h3>
            <p className="card-content">{personalBests?.longest_ride_km || "-" } km</p>
          </CardContent>
        </Card>
      </div>

      <div className="personal-bests-col">
        <Card>
          <CardContent>
            <h3 className="card-header">Fastest Run Pace</h3>
            <p className="card-content">{personalBests?.fastest_run_pace_min_per_km || "-" } min/km</p>
          </CardContent>
        </Card>
      </div>
    </div>
    </div>

  );
};

export default PersonalBests;
