import React, { useState } from 'react'
import PropTypes from 'prop-types'
import TabBar from '../../components/TabBar/TabBar'
import AddItemButton from '../../components/AddItemButton/AddItemButton'
import './Dashboard.css'
import MedicineItem from 'components/MedicineItem/MedicineItem'
import { Button, Pagination } from '@mui/material'
import FilterAltIcon from '@mui/icons-material/FilterAlt';

const Dashboard = props => {
  const [page, setPage] = useState(1);

  return (
    <div className="dashboard-container">
      <TabBar />
      <div className="content-container">
        <div className="content-header">
          <AddItemButton type="inventory" />
          <Pagination count={10} variant="outlined" page={page} onChange={setPage} />
          <Button>
            <FilterAltIcon/>
            Filter
          </Button>
        </div>
        <MedicineItem />
      </div>
    </div>
  )
}

Dashboard.propTypes = {}

export default Dashboard