import React from 'react'
import PropTypes from 'prop-types'
import TabBar from '../../components/TabBar/TabBar'
import AddItemButton from '../../components/AddItemButton/AddItemButton'
import './Dashboard.css'
import MedicineItem from 'components/MedicineItem/MedicineItem'

const Dashboard = props => {
  return (
    <div className="dashboard-container">
        <TabBar/>
        <div className="contennt-container">
          <AddItemButton type="inventory"/>
          <MedicineItem/>
        </div>
    </div>
  )
}

Dashboard.propTypes = {}

export default Dashboard