import React, { useState } from "react";
import { Modal, Box, Typography, TextField, Button } from "@mui/material";
import { AdapterMoment } from '@mui/x-date-pickers/AdapterMoment';
import { DesktopDatePicker, LocalizationProvider } from "@mui/x-date-pickers";

const AddItemForm = ({handleClose}) => {
    const [medicineName, setMedicineName] = useState(null);
    const [expirationDate, setExpirationDate] = useState(null);

    const handleMedicineNameChange = (newMedicineName) => {
        setMedicineName(newMedicineName);
    }

    const handleExpirationDateChange = (newDate) => {
        setExpirationDate(newDate);
    }

    const handleSubmit = () => {
        if (medicineName === null || expirationDate === null) {

        }
        // call api

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
            <LocalizationProvider dateAdapter={AdapterMoment}>
                <DesktopDatePicker
                    label="Expiration date"
                    inputFormat="DD/MM/YYYY"
                    value={expirationDate}
                    onChange={handleExpirationDateChange}
                    renderInput={(params) => <TextField {...params} />}
                    required
                />
            </LocalizationProvider>
            <Box
                sx={{
                    display: 'flex',
                    gap: '1rem',
                    marginLeft: 'auto',
                    marginRight: 0
                }}
            >
                <Button variant="outlined" onClick={handleClose}>Cancel</Button>
                <Button variant="contained" onClick={handleSubmit}>Submit</Button>
            </Box>
        </>
    );
}

export default AddItemForm