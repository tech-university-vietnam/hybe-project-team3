import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { Box, Button, Modal, Typography } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import AddItemForm from 'components/AddWishlistItemForm/AddWishlistItemForm';

const style = {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    boxShadow: 24,
    p: 4,
  };

const AddItemButton = ({handleListChange}) => {
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
                Add item to wishlist
            </Button>
            <Modal
                open={open}
                onClose={handleClose}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <Typography id="modal-modal-title" variant="h6" component="h2">
                        Add item to wishlist
                    </Typography>
                    <AddItemForm handleClose={handleClose} handleListChange={handleListChange} />
                </Box>
            </Modal>
        </>
    )
}

AddItemButton.propTypes = {}

export default AddItemButton