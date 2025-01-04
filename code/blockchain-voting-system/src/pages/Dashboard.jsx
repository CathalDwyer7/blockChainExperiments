import React from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();
  const elections = [
    { id: 1, title: 'Presidential Election 2024', status: 'Ended' },
    { id: 2, title: 'City Council Election', status: 'Ongoing' },
  ];

  const handleVote = (id) => {
    navigate(`/vote/${id}`);
  };

  const handleViewResults = (id) => {
    navigate(`/results/${id}`);
  };

  return (
    <div className="dashboard-container">
      <h1>User Dashboard</h1>
      <ul>
        {elections.map((election) => (
          <li key={election.id}>
            <h3>{election.title}</h3>
            <p>Status: {election.status}</p>
            {election.status === 'Ongoing' && (
              <button onClick={() => handleVote(election.id)}>Vote</button>
            )}
            {election.status === 'Ended' && (
              <button onClick={() => handleViewResults(election.id)}>
                View Results
              </button>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
