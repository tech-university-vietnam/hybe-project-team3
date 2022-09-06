import React from 'react'
import PropTypes from 'prop-types'
import { Button } from '@mui/material'
import AddIcon from '@mui/icons-material/Add'

const AddItemButton = ({onClickHandler, type}) => {
  return (
    <Button variant="outlined" onClick={onClickHandler} startIcon={<AddIcon/>}>
      Add item to {type}
    </Button>
  )
}

AddItemButton.propTypes = {
  type: PropTypes.string,
  onClickHandler: PropTypes.func
}

export default AddItemButton