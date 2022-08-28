import React from 'react'
import PropTypes from 'prop-types'
import { Button } from '@mui/material'

const AddItemButton = props => {
  return (
    <Button variant="contained" onCLick={props.onClickHandler}>Add item to {props.type}</Button>
  )
}

AddItemButton.propTypes = {
    type: PropTypes.string,
    onClickHandler: PropTypes.func
}

export default AddItemButton