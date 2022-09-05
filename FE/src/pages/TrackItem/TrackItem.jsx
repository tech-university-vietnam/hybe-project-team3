import React, { useState } from 'react'
import PropTypes from 'prop-types'
import TabBar from '../../components/TabBar/TabBar'
import AddItemButton from '../../components/AddItemButton/AddItemButton'
import './TrackItem.css'
import MedicineItem from 'components/MedicineItem/MedicineItem'
import { Button, Pagination } from '@mui/material'
import FilterAltIcon from '@mui/icons-material/FilterAlt';

const TrackItem = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const data = Array(10).fill('item');
  console.log(data)

  const handlePageChange = (event, pageNumber) => {
    setCurrentPage(pageNumber)
  }

  return (
    <div className="content-container">
      <div className="content-header">
        <AddItemButton type="inventory" />
        <Pagination count={10} variant="outlined" page={currentPage} onChange={handlePageChange} />
        <Button>
          <FilterAltIcon />
          Filter
        </Button>
      </div>
      <div className="data-container">
        {
          data.map((item) => <MedicineItem name='Sinovac' exp='20/10/2030' />)
        }
      </div>
      <Pagination count={10} variant="outlined" page={currentPage} onChange={handlePageChange} />
    </div>
  )
}

TrackItem.propTypes = {}

export default TrackItem