import React, { useState, useEffect } from 'react';

const AdminDashboard = () => {
  const [elections, setElections] = useState([
    { id: 1, title: 'Presidential Election 2024', status: 'Ongoing', timer: 60 },
    { id: 2, title: 'City Council Election', status: 'Upcoming', timer: 120 },
  ]);
  const [newElection, setNewElection] = useState('');

  useEffect(() => {
    const interval = setInterval(() => {
      setElections((prev) =>
        prev.map((election) => {
          if (election.status === 'Ongoing' && election.timer > 0) {
            return { ...election, timer: election.timer - 1 };
          }
          if (election.timer === 0 && election.status === 'Ongoing') {
            return { ...election, status: 'Ended' };
          }
          return election;
        })
      );
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const handleCreateElection = () => {
    if (newElection) {
      const newId = elections.length + 1;
      setElections([
        ...elections,
        { id: newId, title: newElection, status: 'Upcoming', timer: 0 },
      ]);
      setNewElection('');
    }
  };

  const handleEndElection = (id) => {
    setElections((prev) =>
      prev.map((election) =>
        election.id === id ? { ...election, status: 'Ended' } : election
      )
    );
  };

  const handleDeleteElection = (id) => {
    setElections((prev) => prev.filter((election) => election.id !== id));
  };

  return (
    <div className="admin-dashboard-container">
      <h1>Admin Dashboard</h1>
      <div>
        <input
          type="text"
          placeholder="New Election Title"
          value={newElection}
          onChange={(e) => setNewElection(e.target.value)}
        />
        <button onClick={handleCreateElection}>Create Election</button>
      </div>
      <ul>
        {elections.map((election) => (
          <li key={election.id}>
            <h3>{election.title}</h3>
            <p>Status: {election.status}</p>
            {election.status === 'Ongoing' && (
              <>
                <p>Time Remaining: {election.timer} seconds</p>

                <button onClick={() => handleEndElection(election.id)}>
                  End Election Now
                </button>
              </>
            )}
            <button onClick={() => handleDeleteElection(election.id)}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminDashboard;
