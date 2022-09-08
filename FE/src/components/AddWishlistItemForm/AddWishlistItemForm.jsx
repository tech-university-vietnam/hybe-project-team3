import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { Box, Button, TextField, Typography } from '@mui/material';
import axios from 'axios';
import { postSourceOrder } from 'Utils/api/sourceOrder';

const AddItemForm = ({ handleClose, handleListChange }) => {
    const [medicineName, setMedicineName] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState(false);

    const handleMedicineNameChange = (event) => {
        setError(false);
        setMedicineName(event.target.value);
    }

    const handleSubmit = async () => {
        setIsSubmitting(true);
        await postSourceOrder(medicineName)
            .then((response) => {
                if (response.status > 200 && response.status < 300) {
                    console.log(response.status)
                    setError(false);
                    handleListChange();
                    handleClose();
                }
            })
            .catch(() => setError(true));
        setIsSubmitting(false);

    };

    return (
        <>
            <TextField
                label="Medicine name"
                variant="outlined"
                value={medicineName}
                onChange={handleMedicineNameChange}
                required
            />
            <Box
                sx={{
                    display: "flex",
                    gap: "1rem",
                    marginLeft: "auto",
                    marginRight: 0,
                }}
            >
                <Button variant="outlined" onClick={handleClose}>
                    Cancel
                </Button>
                <Button
                    variant="contained"
                    onClick={handleSubmit}
                    disabled={!medicineName || isSubmitting || error}
                >
                    Submit
                </Button>
            </Box>
            {error && (
                <Typography
                    sx={{
                        color: "red",
                        marginLeft: "auto",
                        marginRight: 0,
                    }}
                >
                    Fail to add this item to the list
                </Typography>
            )}
        </>
    )
}

AddItemForm.propTypes = {
    handleClose: PropTypes.func,
    handleListChange: PropTypes.func
}

export default AddItemForm