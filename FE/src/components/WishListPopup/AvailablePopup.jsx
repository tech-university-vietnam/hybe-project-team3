import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { Box, DialogContent, DialogTitle } from '@mui/material';
import Dialog from '@mui/material/Dialog';
import AvailableHospital from "components/AvailableHospital/AvailableHospital";
import './AvailablePopup.css'
import { getAllNotifications } from "Utils/api/notification";


const AvailablePopup = ({ name }) => {
  const [availableHospitals, setAvailableHospitals] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAPI = async () => {
      const notifications = await getAllNotifications().then(response => response.data);
      const data = notifications.filter((item) => item.type === "notifyAvailable" && item.sourcing_name === name);
      console.log(data);
      setAvailableHospitals(data);
      setIsLoading(false);
    }

    fetchAPI();
  }, []);

  return <Dialog
    open={true}
    // onClose={handleClose}
    fullWidth
    maxWidth="md"
    aria-labelledby="scroll-dialog-title"
    aria-describedby="scroll-dialog-description"
  >
    <DialogTitle id="scroll-dialog-title">{name} is now available</DialogTitle>
    <DialogContent dividers={true}>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: '1rem'}}>
        {isLoading ? <></> : availableHospitals.map((item) =>
          <AvailableHospital
            key={item.id}
            hospital={item.from_hospital.name}
            contact={item.from_hospital.telephone}
            address={item.from_hospital.address}
          />
        )}
      </Box>
    </DialogContent>
  </Dialog>

};

AvailablePopup.propTypes = {};

export default AvailablePopup;
