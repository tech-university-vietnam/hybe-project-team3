import React, { useState } from 'react'
import PropTypes from 'prop-types'
import { Box, Button, TextField, Typography } from '@mui/material'

const AddItemForm = ({handleClose}) => {
    const [medicineName, setMedicineName] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState(false);

    const handleMedicineNameChange = (_, name) => {
        setMedicineName(name)
    }

    const handleSubmit = () => {
        
    }

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

AddItemForm.propTypes = {}

export default AddItemForm