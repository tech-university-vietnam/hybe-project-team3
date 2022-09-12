import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { Box, DialogContent, DialogTitle } from '@mui/material';
import Dialog from '@mui/material/Dialog';
import AvailableHospital from "components/AvailableHospital/AvailableHospital";
import './AvailablePopup.css'
import { getAllNotifications } from "Utils/api/notification";


const AvailablePopup = ({ open, onClose, name, resolve }) => {
  const [availableHospitals, setAvailableHospitals] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getHospitals();
  }, []);

  const getHospitals = async () => {
    setIsLoading(true);
    const notifications = await getAllNotifications().then(response => response.data);
    const data = notifications.filter((item) =>
      item.type === "notifyAvailable" && item.sourcing_name === name && item.status === 'Init');
    setAvailableHospitals(data);
    setIsLoading(false);
  }

  const handleResolve = async () => {
    await resolve();
    onClose(false);
  }

  return <Dialog
    open={open}
    onClose={() => onClose(false)}
    fullWidth
    maxWidth="md"
    aria-labelledby="scroll-dialog-title"
    aria-describedby="scroll-dialog-description"
  >
    <DialogTitle id="scroll-dialog-title">{name} is now available</DialogTitle>
    <DialogContent dividers={true}>
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {isLoading ? <></> : availableHospitals.map((item) =>
          <AvailableHospital
            key={item.id}
            hospital={item.from_hospital.name}
            contact={item.from_hospital.telephone}
            address={item.from_hospital.address}
            id={item.id}
            status={item.status}
            refreshList={getHospitals}
            handleResolve={handleResolve}
          />
        )}
      </Box>
    </DialogContent>
  </Dialog>

};

AvailablePopup.propTypes = {
  open: PropTypes.bool,
  onClose: PropTypes.func,
  name: PropTypes.string,
  resolve: PropTypes.func
};

export default AvailablePopup;
