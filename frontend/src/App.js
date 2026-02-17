// Importáljuk a React-et és a routinghoz szükséges komponenseket a 'react-router-dom'-ból.
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// Importáljuk a különböző oldalainkat (komponenseinket).
import Login from './components/Login';
import Register from './components/Register';
import ShipList from './components/ShipList';
import ShipForm from './components/ShipForm';
import Navbar from './components/Navbar';
// Importáljuk a Bootstrap CSS-t a stílusokhoz.
import 'bootstrap/dist/css/bootstrap.min.css';

// Ez a fő alkalmazás komponens.
function App() {
  return (
    // A <Router> komponens körbeveszi az egész alkalmazást, lehetővé téve az útvonalválasztást (routing).
    <Router>
      {/* A Navbar minden oldalon meg fog jelenni, mert a <Routes> felett van. */}
      <Navbar />
      {/* Ez a konténer a Bootstrap-től jön, és szépen középre igazítja a tartalmat. */}
      <div className="container">
        {/* A <Routes> komponens felelős a megfelelő oldal (Route) kiválasztásáért az URL alapján. */}
        <Routes>
          {/* Ha az URL '/login', a <Login> komponenst rendereli. */}
          <Route path="/login" element={<Login />} />
          {/* Ha az URL '/register', a <Register> komponenst rendereli. */}
          <Route path="/register" element={<Register />} />
          {/* Ha az URL '/ships', a <ShipList> komponenst rendereli. */}
          <Route path="/ships" element={<ShipList />} />
          {/* Ha az URL '/ships/new', a <ShipForm> komponenst rendereli új hajó létrehozásához. */}
          <Route path="/ships/new" element={<ShipForm />} />
          {/* Ha az URL '/ships/edit/valami', a <ShipForm> komponenst rendereli szerkesztéshez. Az ':id' egy URL paraméter. */}
          <Route path="/ships/edit/:id" element={<ShipForm />} />
          {/* Ha az URL a gyökér ('/'), automatikusan átirányít a '/ships' útvonalra. */}
          <Route path="/" element={<Navigate to="/ships" />} />
        </Routes>
      </div>
    </Router>
  );
}

// Exportáljuk az App komponenst, hogy az index.js használni tudja.
export default App;