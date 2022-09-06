import React, { useState } from "react";
import { Modal, Box, Typography, TextField, Button } from "@mui/material";
import { AdapterMoment } from '@mui/x-date-pickers/AdapterMoment';
import { DesktopDatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import axios from "axios";
import moment from "moment";

let addTrackingMedicineUrl = 'http://localhost:8000/tracking-medicine'

const AddItemForm = ({ handleClose }) => {
    const [medicineName, setMedicineName] = useState('');
    const [expirationDate, setExpirationDate] = useState(null);
    
    const handleMedicineNameChange = (event) => {
        setMedicineName(event.target.value);
    }

    const handleExpirationDateChange = (newDate) => {
        setExpirationDate(newDate);
    }

    const handleSubmit = async () => {
        if (medicineName === null || expirationDate === null) {

        }
        const date = moment(expirationDate).format('YYYY-MM-DDTHH:MM:SSZ')
        await postTrackingMedicine(date);
    }

    const postTrackingMedicine = async (date) => {
        
        const body = {
            "name": medicineName,
            "expirationDate": date
        }
        console.log(body)
        // await axios.post(addTrackingMedicineUrl, body)
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
                <Button variant="contained" onClick={handleSubmit} disabled={!medicineName || !expirationDate}>Submit</Button>
            </Box>
        </>
    );
}

export default AddItemForm