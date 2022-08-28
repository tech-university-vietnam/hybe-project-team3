import React from "react";
import "./HomePage.css";
import Login from "pages/Login/Login";
import Register from "pages/Register/Register";
import Dashboard from "pages/Dashboard/Dashboard"
import { Footer } from "layouts/Footer/Footer";
import Header from "../../layouts/Header/Header";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

export const HomePage = () => (
  <Router>
    <div className='page-container'>
      <Header />
      <Dashboard />
      {/* <Routes>
      <Route index element={<Login />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
    </Routes>
    <Footer /> */}
    </div>

  </Router>
);
