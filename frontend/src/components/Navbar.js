import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';

const Navbar = () => {
    const navigate = useNavigate();
    const token = localStorage.getItem('access_token');

    const handleLogout = async () => {
        try {
            await api.delete('/auth/logout');
        } catch (error) {
            console.error("Error during logout (token probably expired):", error);
        } finally {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            navigate('/login');
            window.location.reload(); // Reload the page to re-render the Navbar
        }
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light mb-4">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/ships">Ship Manager</Link>
                <div className="d-flex">
                    {token ? (
                        <button onClick={handleLogout} className="btn btn-outline-danger">Logout</button>
                    ) : (
                        <>
                            <Link to="/login" className="btn btn-outline-success me-2">Login</Link>
                            <Link to="/register" className="btn btn-outline-primary">Register</Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;