import React from 'react'
import PropTypes from 'prop-types'
import { Button } from '@mui/material'
import AddIcon from '@mui/icons-material/Add'

const AddItemButton = props => {
  return (
    <Button variant="contained" onClick={props.onClickHandler} startIcon={<AddIcon/>}>
      Add item to {props.type}
    </Button>
  )
}

AddItemButton.propTypes = {
  type: PropTypes.string,
  onClickHandler: PropTypes.func
}

export default AddItemButton