// Import necessary React hooks and components.
import React, { useState } from 'react';
// useState: for state management.
import { useNavigate, Link } from 'react-router-dom'; // useNavigate: for programmatic navigation; Link: for navigation links.
import api from '../api'; // Our axios client.

// The Login component.
const Login = () => {
    // Define 'State' variables with the 'useState' hook.
    // 'username' stores the value of the input field, and 'setUsername' is the function to update it.
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(''); // For storing error messages.
    const navigate = useNavigate(); // We will use the 'navigate' function for redirections.

    // This function runs when the user submits the form.
    const handleSubmit = async (e) => {
        e.preventDefault(); // Prevent the page from reloading on form submission.
        try {
            // Send an asynchronous request to the '/auth/login' endpoint with the 'api' client.
            const response = await api.post('/auth/login', { username, password });
            // If the request is successful, save the received tokens to the browser's localStorage.
            // localStorage is a simple key-value store that persists even after the browser is closed.
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('refresh_token', response.data.refresh_token);
            // Redirect the user to the '/ships' page.
            navigate('/ships');
        } catch (err) {
            // If the login fails (e.g., wrong password), the 'catch' block runs.
            // We set an error message that will be displayed to the user.
            setError('Invalid username or password!');
        }
    };

    // The component's JSX code, which renders the HTML.
    return (
        <div className="col-md-6 offset-md-3 mt-5">
            <h2>Admin Login</h2>
            {/* Conditional rendering: the error message only appears if the 'error' state is not empty. */}
            {error && <div className="alert alert-danger">{error}</div>}
            {/* The form, which binds the 'handleSubmit' function to the 'onSubmit' event. */}
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Username</label>
                    {/* The input field's 'value' is bound to the 'username' state. */}
                    {/* The 'onChange' event updates the state with every keystroke. */}
                    <input type="text" className="form-control" value={username} onChange={(e) => setUsername(e.target.value)} required />
                </div>
                <div className="mb-3">
                    <label className="form-label">Password</label>
                    <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <button type="submit" className="btn btn-primary">Login</button>
            </form>
            <div className="mt-3">
                {/* The <Link> component creates a navigation link to the registration page. */}
                <p>Don't have an account yet? <Link to="/register">Register here!</Link></p>
            </div>
        </div>
    );
};

// Export the component.
export default Login;