import React, { useState } from "react";
import "./HomePage.css";
import Header from "../../layouts/Header/Header";
import TabBar from '../../components/TabBar/TabBar'
import TrackedList from "pages/TrackedList/TrackedList";
import WishList from "pages/WishList/WishList";
import { Box } from "@mui/system";

const dashboard = {
  'tracked-list': <TrackedList />,
  'wishlist': <WishList />,
}

export const HomePage = () => {
  const [currentTab, setCurrentTab] = useState('tracked-list')

  const handleChangeTab = (tab) => {
    setCurrentTab(tab);
  }

  return (
    <div className='page-container'>
      <TabBar className='tab-bar' currentTab={currentTab} handleChangeTab={handleChangeTab} />
      <div className='dashboard-container'>
        <Header />
        <Box sx={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          {dashboard[currentTab]}

        </Box>
      </div>
    </div>
  );
}