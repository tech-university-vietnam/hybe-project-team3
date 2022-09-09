import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import { Box, IconButton, Modal, Typography } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { Close } from "@mui/icons-material";

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
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

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
    }
  ]);

  useEffect(() => {}, []);

  return <Modal
    open={true}
    // onClose={handleClose}
    aria-labelledby="modal-modal-title"
    aria-describedby="modal-modal-description"
  >
    <Box sx={style}>
      <Typography id="modal-modal-title" variant="h6" component="h2">
        Panadol
      </Typography>
      
    </Box>
  </Modal>;
};

AvailablePopup.propTypes = {};

export default AvailablePopup;
