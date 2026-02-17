// Importáljuk a szükséges React hook-okat és komponenseket.
import React, { useState } from 'react';
// useState: állapot (state) kezelésére.
import { useNavigate, Link } from 'react-router-dom'; // useNavigate: programozott átirányításhoz; Link: navigációs linkekhez.
import api from '../api'; // Az axios kliensünk.

// A Login komponens.
const Login = () => {
    // 'State' változók definiálása a 'useState' hook-kal.
    // A 'username' tárolja az input mező értékét, a 'setUsername' pedig a frissítésére szolgáló függvény.
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(''); // Hibaüzenetek tárolására.
    const navigate = useNavigate(); // A 'navigate' függvényt az átirányításokhoz fogjuk használni.

    // Ez a függvény fut le, amikor a felhasználó elküldi az űrlapot.
    const handleSubmit = async (e) => {
        e.preventDefault(); // Megakadályozzuk az oldal újratöltődését az űrlap elküldésekor.
        try {
            // Aszinkron kérést küldünk a '/auth/login' végpontra az 'api' klienssel.
            const response = await api.post('/auth/login', { username, password });
            // Ha a kérés sikeres, elmentjük a kapott tokeneket a böngésző localStorage-ába.
            // A localStorage egy egyszerű kulcs-érték tároló, ami a böngésző bezárása után is megmarad.
            localStorage.setItem('access_token', response.data.access_token);
            localStorage.setItem('refresh_token', response.data.refresh_token);
            // Átirányítjuk a felhasználót a '/ships' oldalra.
            navigate('/ships');
        } catch (err) {
            // Ha a bejelentkezés sikertelen (pl. rossz jelszó), a 'catch' blokk fut le.
            // Beállítunk egy hibaüzenetet, ami megjelenik a felhasználónak.
            setError('Hibás felhasználónév vagy jelszó!');
        }
    };

    // A komponens JSX kódja, ami a HTML-t rendereli.
    return (
        <div className="col-md-6 offset-md-3 mt-5">
            <h2>Admin Bejelentkezés</h2>
            {/* Feltételes renderelés: a hibaüzenet csak akkor jelenik meg, ha az 'error' state nem üres. */}
            {error && <div className="alert alert-danger">{error}</div>}
            {/* Az űrlap, ami beköti a 'handleSubmit' függvényt az 'onSubmit' eseményre. */}
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Felhasználónév</label>
                    {/* Az input mező 'value'-ja a 'username' state-hez van kötve. */}
                    {/* Az 'onChange' esemény minden billentyűleütéskor frissíti a state-et. */}
                    <input type="text" className="form-control" value={username} onChange={(e) => setUsername(e.target.value)} required />
                </div>
                <div className="mb-3">
                    <label className="form-label">Jelszó</label>
                    <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} required />
                </div>
                <button type="submit" className="btn btn-primary">Belépés</button>
            </form>
            <div className="mt-3">
                {/* A <Link> komponens egy navigációs linket hoz létre a regisztrációs oldalra. */}
                <p>Nincs még fiókod? <Link to="/register">Regisztrálj itt!</Link></p>
            </div>
        </div>
    );
};

// Exportáljuk a komponenst.
export default Login;