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
            console.error("Hiba a kijelentkezés során (token valószínűleg lejárt):", error);
        } finally {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            navigate('/login');
            window.location.reload(); // Frissítjük az oldalt, hogy a Navbar újrarenderelődjön
        }
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light mb-4">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/ships">Hajó Menedzser</Link>
                <div className="d-flex">
                    {token ? (
                        <button onClick={handleLogout} className="btn btn-outline-danger">Kijelentkezés</button>
                    ) : (
                        <>
                            <Link to="/login" className="btn btn-outline-success me-2">Bejelentkezés</Link>
                            <Link to="/register" className="btn btn-outline-primary">Regisztráció</Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;