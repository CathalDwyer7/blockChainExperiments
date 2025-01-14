import React, { useState } from 'react';
import { useParams } from 'react-router-dom';

const Vote = () => {
  const { id } = useParams(); // Get election ID from URL parameters
  const [proposals, setProposals] = useState([
    { id: 1, title: 'Proposal A', votes: 0 },
    { id: 2, title: 'Proposal B', votes: 0 },
    { id: 3, title: 'Proposal C', votes: 0 },
  ]);
  const [credits, setCredits] = useState(20);

  const calculateCost = (votes) => votes * votes;

  const handleVote = (proposalId, increment) => {
    setProposals((prev) =>
      prev.map((proposal) => {
        if (proposal.id === proposalId) {
          const newVotes = proposal.votes + increment;
          const cost = calculateCost(newVotes) - calculateCost(proposal.votes);
          if (credits >= cost && newVotes >= 0) {
            setCredits((prevCredits) => prevCredits - cost);
            return { ...proposal, votes: newVotes };
          }
        }
        return proposal;
      })
    );
  };

  const handleSubmit = () => {
    alert('Votes submitted successfully!');
    // Here, you'd typically send the votes to your backend.
  };

  return (
    <div className="vote-container">
      <h1>Quadratic Voting for Election {id}</h1>
      <p>Credits Remaining: {credits}</p>
      <ul>
        {proposals.map((proposal) => (
          <li key={proposal.id}>
            <h3>{proposal.title}</h3>
            <p>Votes: {proposal.votes}</p>
            <button onClick={() => handleVote(proposal.id, 1)}>+1 Vote</button>
            <button onClick={() => handleVote(proposal.id, -1)}>-1 Vote</button>
          </li>
        ))}
      </ul>
      <button onClick={handleSubmit} disabled={credits < 0}>
        Submit Votes
      </button>
    </div>
  );
};

export default Vote;
