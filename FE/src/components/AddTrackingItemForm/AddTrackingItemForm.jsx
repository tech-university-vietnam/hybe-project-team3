import React, { useState } from "react";
import PropTypes from "prop-types";
import { Box, Typography, TextField, Button } from "@mui/material";
import { AdapterMoment } from "@mui/x-date-pickers/AdapterMoment";
import { DesktopDatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import axios from "axios";
import moment from "moment";
import { postTrackingMedicine } from "Utils/api/medicine";

const AddItemForm = ({ handleClose, handleListChange }) => {
  const [medicineName, setMedicineName] = useState("");
  const [expirationDate, setExpirationDate] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(false);

  const handleMedicineNameChange = (event) => {
    setError(false);
    setMedicineName(event.target.value);
  };

  const handleExpirationDateChange = (newDate) => {
    setError(false);
    setExpirationDate(newDate);
  };

  const handleSubmit = async () => {
    const date = moment(expirationDate).format("YYYY-MM-DDTHH:MM:SSZ");
    setIsSubmitting(true);
    await postTrackingMedicine(medicineName, date)
      .then((response) => {
        if (response.status > 200 && response.status < 300) {
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
          disabled={!medicineName || !expirationDate || isSubmitting || error}
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
  );
};

AddItemForm.propTypes = {
  handleClose: PropTypes.func,
  handleListChange: PropTypes.func,
};

export default AddItemForm;
