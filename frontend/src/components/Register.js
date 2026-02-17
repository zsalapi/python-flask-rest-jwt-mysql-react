// Import necessary React hooks and components.
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api'; // Our axios client.

// The Register component.
const Register = () => {
    // State variables for form data, as well as success and error messages.
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    // Function that runs when the form is submitted.
    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent the page from reloading.
        // Clear previous messages on each new attempt.
        setError('');
        setSuccess('');
        try {
            // Send a request to the '/api/users' endpoint with the new user's data.
            await api.post('/api/users', { name, password });
            // On successful registration, set a success message.
            setSuccess('Registration successful! You can now log in.');
            // Wait 2 seconds, then redirect the user to the login page.
            setTimeout(() => navigate('/login'), 2000);
        } catch (err) {
            // In case of an error, read the error message sent by the backend, if any.
            if (err.response && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                // If there is no specific error message, display a generic one.
                setError('An error occurred during registration.');
            }
        }
    };

    // The component's JSX code.
    return (
        <div className="col-md-6 offset-md-3 mt-5">
            <h2>Register</h2>
            {/* Conditional rendering for error and success messages. */}
            {error && <div className="alert alert-danger">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Username</label>
                    <input type="text" className="form-control" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <div className="mb-3">
                    <label className="form-label">Password</label>
                    <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <button type="submit" className="btn btn-primary">Register</button>
            </form>
            <div className="mt-3">
                <p>Already have an account? <Link to="/login">Log in!</Link></p>
            </div>
        </div>
    );
};

export default Register;