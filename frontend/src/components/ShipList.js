import React, { useEffect, useState, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';

const ShipList = () => {
    const [ships, setShips] = useState([]);
    const navigate = useNavigate();

    const fetchShips = useCallback(async () => {
        try {
            const response = await api.get('/api/ships');
            setShips(response.data);
        } catch (error) {
            console.error("Hiba a hajók lekérésekor", error);
            if (error.response && error.response.status === 401) {
                navigate('/login');
            }
        }
    }, [navigate]);

    useEffect(() => {
        fetchShips();
    }, [fetchShips]);

    const handleDelete = async (id) => {
        if (window.confirm('Biztosan törölni szeretnéd ezt a hajót?')) {
            try {
                await api.delete(`/api/ships/${id}`);
                fetchShips();
            } catch (error) {
                console.error("Hiba a törléskor", error);
            }
        }
    };

    return (
        <div className="mt-4">
            <h2>Hajók Listája</h2>
            <Link to="/ships/new" className="btn btn-success mb-3">Új Hajó Hozzáadása</Link>
            <ul className="list-group">
                {ships.map(ship => (
                    <li key={ship.id} className="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <strong>{ship.model}</strong> - {ship.ship_class} ({ship.affiliation})
                        </div>
                        <div>
                            <Link to={`/ships/edit/${ship.id}`} className="btn btn-sm btn-warning me-2">Szerkesztés</Link>
                            <button onClick={() => handleDelete(ship.id)} className="btn btn-sm btn-danger">Törlés</button>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ShipList;