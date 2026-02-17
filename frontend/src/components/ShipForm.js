import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import api from '../api';

const ShipForm = () => {
    const [ship, setShip] = useState({
        model: '',
        ship_class: '',
        affiliation: '',
        manufacturer: '',
        category: '',
        crew: 0,
        length: 0,
        roles: ''
    });
    const { id } = useParams();
    const navigate = useNavigate();

    const fetchShip = useCallback(async () => {
        try {
            const response = await api.get(`/api/ships/${id}`);
            const data = response.data;
            // Convert roles array to string for editing
            if (Array.isArray(data.roles)) {
                data.roles = data.roles.join(', ');
            }
            setShip(data);
        } catch (error) {
            console.error("Error loading ship", error);
        }
    }, [id]);

    useEffect(() => {
        if (id) {
            fetchShip();
        }
    }, [id, fetchShip]);

    const handleChange = (e) => {
        setShip({ ...ship, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const payload = { ...ship };
        // Convert roles string back to an array
        if (typeof payload.roles === 'string') {
            payload.roles = payload.roles.split(',').map(role => role.trim());
        }

        try {
            if (id) {
                await api.put(`/api/ships/${id}`, payload);
            } else {
                await api.post('/api/ships', payload);
            }
            navigate('/ships');
        } catch (error) {
            console.error("Error saving ship", error);
        }
    };

    return (
        <div className="col-md-8 offset-md-2 mt-4">
            <h2>{id ? 'Edit Ship' : 'New Ship'}</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Model</label>
                    <input name="model" className="form-control" value={ship.model} onChange={handleChange} required />
                </div>
                <div className="mb-3">
                    <label className="form-label">Class</label>
                    <input name="ship_class" className="form-control" value={ship.ship_class} onChange={handleChange} required />
                </div>
                <div className="mb-3">
                    <label className="form-label">Affiliation</label>
                    <input name="affiliation" className="form-control" value={ship.affiliation} onChange={handleChange} />
                </div>
                <div className="mb-3">
                    <label className="form-label">Roles (comma-separated)</label>
                    <input name="roles" className="form-control" value={ship.roles} onChange={handleChange} />
                </div>
                <button type="submit" className="btn btn-primary">Save</button>
            </form>
        </div>
    );
};

export default ShipForm;