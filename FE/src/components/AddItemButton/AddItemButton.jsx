import React, { useState } from 'react';
import PropTypes from 'prop-types';
import AddIcon from '@mui/icons-material/Add';
import { Modal, Box, Typography, Button } from "@mui/material";
import AddItemForm from 'components/AddItemForm/AddItemForm';
import { faCircleXmark } from '@fortawesome/free-solid-svg-icons';

const style = {
  display: 'flex',
  flexDirection: 'column',
  gap: '1rem',
  position: 'absolute',
  top: '50%',
  left: '50%',
  gap: '1rem',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

const AddItemButton = ({ type }) => {
  const [open, setOpen] = useState(false);

  const onAddButtonClick = () => {
    setOpen(true);
  }

  const handleClose = () => {
    setOpen(false);
  }

  return (
    <>
      <Button variant="outlined" onClick={onAddButtonClick} startIcon={<AddIcon />}>
        Add item to {type}
      </Button>
      <Modal
            open={open}
            onClose={handleClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
            <Box sx={style}>
                <Typography id="modal-modal-title" variant="h6" component="h2">
                    Add an item to tracked list
                </Typography>
                <AddItemForm handleClose={handleClose}/>
            </Box>
        </Modal>
    </>
  )
}

AddItemButton.propTypes = {
  type: PropTypes.string,
  onClickHandler: PropTypes.func
}

export default AddItemButton