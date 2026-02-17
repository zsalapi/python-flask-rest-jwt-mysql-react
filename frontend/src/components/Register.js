// Importáljuk a szükséges React hook-okat és komponenseket.
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../api'; // Az axios kliensünk.

// A Register komponens.
const Register = () => {
    // State változók az űrlap adataihoz, valamint a siker- és hibaüzenetekhez.
    const [name, setName] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    // Az űrlap elküldésekor lefutó függvény.
    const handleSubmit = async (e) => {
        e.preventDefault(); // Megakadályozzuk az oldal újratöltődését.
        // Töröljük a korábbi üzeneteket minden új próbálkozásnál.
        setError('');
        setSuccess('');
        try {
            // Kérést küldünk a '/api/users' végpontra az új felhasználó adataival.
            await api.post('/api/users', { name, password });
            // Sikeres regisztráció esetén beállítunk egy sikerüzenetet.
            setSuccess('Sikeres regisztráció! Most már bejelentkezhetsz.');
            // Várunk 2 másodpercet, majd átirányítjuk a felhasználót a bejelentkezési oldalra.
            setTimeout(() => navigate('/login'), 2000);
        } catch (err) {
            // Hiba esetén kiolvassuk a backend által küldött hibaüzenetet, ha van.
            if (err.response && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                // Ha nincs specifikus hibaüzenet, egy általánosat jelenítünk meg.
                setError('Hiba történt a regisztráció során.');
            }
        }
    };

    // A komponens JSX kódja.
    return (
        <div className="col-md-6 offset-md-3 mt-5">
            <h2>Regisztráció</h2>
            {/* Feltételes renderelés a hiba- és sikerüzeneteknek. */}
            {error && <div className="alert alert-danger">{error}</div>}
            {success && <div className="alert alert-success">{success}</div>}
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Felhasználónév</label>
                    <input type="text" className="form-control" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>
                <div className="mb-3">
                    <label className="form-label">Jelszó</label>
                    <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <button type="submit" className="btn btn-primary">Regisztráció</button>
            </form>
            <div className="mt-3">
                <p>Már van fiókod? <Link to="/login">Jelentkezz be!</Link></p>
            </div>
        </div>
    );
};

export default Register;