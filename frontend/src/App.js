// Import React and the necessary components for routing from 'react-router-dom'.
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// Import our different pages (components).
import Login from './components/Login';
import Register from './components/Register';
import ShipList from './components/ShipList';
import ShipForm from './components/ShipForm';
import Navbar from './components/Navbar';
// Import Bootstrap CSS for styling.
import 'bootstrap/dist/css/bootstrap.min.css';

// This is the main application component.
function App() {
  return (
    // The <Router> component wraps the entire application, enabling routing.
    <Router>
      {/* The Navbar will appear on every page because it is above <Routes>. */}
      <Navbar />
      {/* This container comes from Bootstrap and nicely centers the content. */}
      <div className="container">
        {/* The <Routes> component is responsible for selecting the appropriate page (Route) based on the URL. */}
        <Routes>
          {/* If the URL is '/login', it renders the <Login> component. */}
          <Route path="/login" element={<Login />} />
          {/* If the URL is '/register', it renders the <Register> component. */}
          <Route path="/register" element={<Register />} />
          {/* If the URL is '/ships', it renders the <ShipList> component. */}
          <Route path="/ships" element={<ShipList />} />
          {/* If the URL is '/ships/new', it renders the <ShipForm> component for creating a new ship. */}
          <Route path="/ships/new" element={<ShipForm />} />
          {/* If the URL is '/ships/edit/something', it renders the <ShipForm> component for editing. The ':id' is a URL parameter. */}
          <Route path="/ships/edit/:id" element={<ShipForm />} />
          {/* If the URL is the root ('/'), it automatically redirects to the '/ships' route. */}
          <Route path="/" element={<Navigate to="/ships" />} />
        </Routes>
      </div>
    </Router>
  );
}

// Export the App component so that index.js can use it.
export default App;