import React, { useState } from 'react'
import AddItemButton from '../../components/AddItemButton/AddItemButton'
import './TrackedList.css'
import MedicineItem from 'components/MedicineItem/MedicineItem'
import { Button, Pagination } from '@mui/material'
import FilterAltIcon from '@mui/icons-material/FilterAlt'

const TrackedList = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const data = Array(10).fill('item');
  console.log(data)

  const handlePageChange = (_, pageNumber) => {
    setCurrentPage(pageNumber)
  }

  return (
    <div className="content-container">
      <div className="content-header">
        <AddItemButton type="tracked list" />
        <Pagination count={10} variant="outlined" page={currentPage} onChange={handlePageChange} />
        <Button>
          <FilterAltIcon />
          Filter
        </Button>
      </div>
      <div className="data-container">
        {
          data.map((item) => <MedicineItem name='Sinovac' expirationDate='20/10/2030' />)
        }
      </div>
      <Pagination count={10} variant="outlined" page={currentPage} onChange={handlePageChange} />
    </div>
  )
}

TrackedList.propTypes = {}

export default TrackedList