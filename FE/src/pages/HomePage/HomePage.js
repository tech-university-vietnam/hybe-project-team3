import React from "react";
import "./HomePage.css";
import Login from "pages/Login/Login";
import Register from "pages/Register/Register";
import { Footer } from "layouts/Footer/Footer";
import Header from "../../layouts/Header/Header";
import TabBar from '../../components/TabBar/TabBar'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TrackedList from "pages/TrackedList/TrackedList";

export const HomePage = () => (
  <Router>
    <div className='page-container'>
      <TabBar className='tab-bar'/>
      <div className='dashboard-container'>
        <Header />
        <TrackedList />
      </div>
    </div>
  </Router>
);
