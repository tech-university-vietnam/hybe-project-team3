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

const ResolvedPopup = ({
  id,
  popupData: {
    name: medicineName,
    expired_date: expirationDate,
    hospital: {
      name: hospitalName,
      telephone: hospitalPhone,
      address: hospitalAddress,
    },
  },
  open,
  onClose,
}) => {
  return (
    <Modal open={open} onClose={() => onClose(false)}>
      <Box sx={style}>
        <Typography sx={{ fontWeight: "bold" }}>
          🎉 You've bought {medicineName} from {hospitalName}
        </Typography>
        <Typography>Expiration date: {expirationDate}</Typography>
        <Typography>Address: {hospitalAddress}</Typography>
        <Typography>Contact number: {hospitalPhone}</Typography>
      </Box>
    </Modal>
  );
};

ResolvedPopup.propTypes = {
  id: PropTypes.number,
  hospitalName: PropTypes.string,
  hospitalAddress: PropTypes.string,
  hospitalPhone: PropTypes.string,
  medicineName: PropTypes.string,
  expirationDate: PropTypes.string,
};

export default ResolvedPopup;
