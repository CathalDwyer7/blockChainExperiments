import React from 'react';
import { useParams } from 'react-router-dom';

const Results = () => {
  const { id } = useParams(); // Get election ID from URL parameters
  const results = {
    1: [
      { proposal: 'Proposal A', votes: 50 },
      { proposal: 'Proposal B', votes: 30 },
      { proposal: 'Proposal C', votes: 20 },
    ],
    2: [
      { proposal: 'Proposal X', votes: 100 },
      { proposal: 'Proposal Y', votes: 60 },
    ],
  };

  return (
    <div className="results-container">
      <h1>Election Results for Election {id}</h1>
      <ul>
        {results[id]?.map((result, index) => (
          <li key={index}>
            <strong>{result.proposal}</strong>: {result.votes} votes
          </li>
        )) || <p>No results available for this election.</p>}
      </ul>
    </div>
  );
};

export default Results;
