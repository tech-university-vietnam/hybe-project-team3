import React, { useState } from "react";
import "./HomePage.css";
import Login from "pages/Login/Login";
import Register from "pages/Register/Register";
import { Footer } from "layouts/Footer/Footer";
import Header from "../../layouts/Header/Header";
import TabBar from '../../components/TabBar/TabBar'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import TrackedList from "pages/TrackedList/TrackedList";
import WishList from "pages/WishList/WishList";
import Notification from "pages/Notification/Notification";

export const HomePage = () => {
  const dashboard = {
    'tracked-list': <TrackedList/>,
    'wishlist': <WishList/>,
    'notification': <Notification/>
  }
  const [currentTab, setCurrentTab] = useState('tracked-list')

  const handleChangeTab = (tab) => {
    setCurrentTab(tab);
  }

  return (
    <div className='page-container'>
      <TabBar className='tab-bar' currentTab={currentTab} handleChangeTab={handleChangeTab}/>
      <div className='dashboard-container'>
        <Header />
        {dashboard[currentTab]}
      </div>
    </div>
  );
}