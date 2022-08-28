import React from 'react'
import PropTypes from 'prop-types'
import TabBar from '../../components/TabBar/TabBar'
import AddItemButton from '../../components/AddItemButton/AddItemButton'
import './Dashboard.css'

const Dashboard = props => {
  return (
    <div className="dashboard-container">
        <TabBar/>
        <div className="contennt-container">
          Place holder 
          <AddItemButton/>
        </div>
    </div>
  )
}

Dashboard.propTypes = {}

export default Dashboard