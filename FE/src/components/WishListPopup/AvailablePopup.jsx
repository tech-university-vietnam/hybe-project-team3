import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { Box, DialogContent, DialogTitle } from '@mui/material';
import Dialog from '@mui/material/Dialog';
import AvailableHospital from "components/AvailableHospital/AvailableHospital";
import './AvailablePopup.css'


const AvailablePopup = (props) => {
  const [availableHospitals, setAvailableHospitals] = useState([
    {
      id: 1,
      hospital: "Hospital",
      contact: "0123 456 789",
      expired: "12/12/2022"
    },
    {
      id: 2,
      hospital: "Hospital",
      contact: "0123 456 789",
      expired: "12/12/2022"
    },
    {
      id: 3,
      hospital: "Hospital",
      contact: "0123 456 789",
      expired: "12/12/2022"
    },
    {
      id: 4,
      hospital: "Hospital",
      contact: "0123 456 789",
      expired: "12/12/2022"
    },
    {
      id: 5,
      hospital: "Hospital",
      contact: "0123 456 789",
      expired: "12/12/2022"
    },
    {
      id: 6,
      hospital: "Hospital",
      contact: "0123 456 789",
      expired: "12/12/2022"
    },
    {
      id: 7,
      hospital: "Hospital",
      contact: "0123 456 789",
      expired: "12/12/2022"
    }
  ]);

  useEffect(() => { }, []);

  return <Dialog
    open={true}
    // onClose={handleClose}
    aria-labelledby="scroll-dialog-title"
    aria-describedby="scroll-dialog-description"
  >
    <DialogTitle id="scroll-dialog-title">Medicine name</DialogTitle>
    <DialogContent dividers={true}>
      <Box sx={{display: 'flex', flexDirection: 'column', gap: '1rem'}}>
      {availableHospitals.map((item) =>
        <AvailableHospital
          key={item.id}
          hospital={item.hospital}
          contact={item.contact}
          expired={item.expired} />
      )}
      </Box>
    </DialogContent>
  </Dialog>

};

AvailablePopup.propTypes = {};

export default AvailablePopup;
