import React from "react";
import "./HomePage.css";
import Header from "../../layouts/Header/Header";
import TabBar from '../../components/TabBar/TabBar'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TrackedList from "pages/TrackItem/TrackedList";

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
