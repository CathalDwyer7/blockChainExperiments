import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App'; // Your main application component
import './index.css'; // Optional: Import global CSS styles

// Find the root element in the public/index.html file
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the React app into the DOM
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
