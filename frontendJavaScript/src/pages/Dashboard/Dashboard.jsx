import React, { useEffect, useState } from 'react';
import { Loader } from 'lucide-react';
import './Dashboard.css'; 
import PersonalBests from '../../components/PersonalBests/PersonalBests.jsx';

const Dashboard = () => {
  const [personalBests, setPersonalBests] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const resPBs = await fetch('http://localhost:5001/dashboard/personal_bests');
        const pbData = await resPBs.json();

        setPersonalBests(pbData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data', error);
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">My Strava Dashboard</h1>

      {loading ? (
        <div className="dashboard-loading">
          <Loader className="animate-spin text-muted" size={48} />
        </div>
      ) : (
        <PersonalBests personalBests={personalBests} />
      )}
    </div>
  );
};

export default Dashboard;
