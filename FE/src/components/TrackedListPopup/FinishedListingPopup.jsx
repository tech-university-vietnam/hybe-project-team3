import React from "react";
import PropTypes from "prop-types";
import { Box, Modal, Typography } from "@mui/material";

const style = {
  display: "flex",
  flexDirection: "column",
  gap: "1rem",
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  boxShadow: 24,
  p: 4,
};

const FinishedListingPopup = ({ id, popupData, open, onClose }) => {
  if (popupData === undefined) {
    return <div>Loading...</div>;
  }
  const {
    name: medicineName,
    hospital: {
      name: hospitalName,
      address: hospitalAddress,
      telephone: hospitalPhone,
    },
  } = popupData;
  return (
    <Modal open={open} onClose={() => onClose(false)}>
      <Box sx={style}>
        <Typography sx={{ fontWeight: "bold" }}>
          🎉 {hospitalName} bought {medicineName} from you!
        </Typography>
        <Typography>Address: {hospitalAddress}</Typography>
        <Typography>Contact number: {hospitalPhone}</Typography>
      </Box>
    </Modal>
  );
};

FinishedListingPopup.propTypes = {
  id: PropTypes.number,
  hospitalName: PropTypes.string,
  hospitalAddress: PropTypes.string,
  hospitalPhone: PropTypes.string,
  medicineName: PropTypes.string,
  expirationDate: PropTypes.string,
};

export default FinishedListingPopup;
