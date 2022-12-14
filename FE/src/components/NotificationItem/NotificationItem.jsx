import React from "react";
import PropTypes from "prop-types";
import { Button, Typography, Paper } from "@mui/material";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import {
  postApproveNotification,
  postDeclineNotification,
} from "Utils/api/notification";

const NotificationItem = ({
  id,
  sourcingId,
  trackingMedicineId,
  fromHospital,
  toHospital,
  medicineName,
  typeOfNotification,
  status,
  onApproveDecline,
  openPopup,
  getBuyingHospitalData,
}) => {
  const onDecline = async ({ id }) => {
    try {
      await postDeclineNotification({ id });
      await onApproveDecline();
    } catch ({response}) {
      alert(response.data)
    }
  };

  const getHospitalName = () => {
    switch (typeOfNotification) {
      case "warningExpired":
        return fromHospital.name;
      case "notifyAvailable":
        return toHospital.name;
      default:
        return "";
    }
  };

  const getPopupId = () => {
    switch (typeOfNotification) {
      case "warningExpired":
        return trackingMedicineId;
      case "notifyAvailable":
        return sourcingId;
      case "notifySold":
        return trackingMedicineId;
      default:
        return trackingMedicineId;
    }
  };

  const onApprove = async ({ id }) => {
    try {
      await postApproveNotification({ id });
      await onApproveDecline();
    } catch ({response}) {
      alert(response.data)
    }
  };

  if (typeOfNotification === "warningExpired") {
    return (
      <div>
        {medicineName} in your Tracked List is about to expire!
        {status === "Init" && (
          <div>
            <Button onClick={() => onDecline({ id })} startIcon={<CloseIcon />}>
              Cancel
            </Button>
            <Button onClick={() => onApprove({ id })} startIcon={<CheckIcon />}>
              List
            </Button>
          </div>
        )}
        {status === "Declined" && (
          <Typography variant="subtitle2" color="orange">
            ❌ You've declined to list this item
          </Typography>
        )}
        {status === "Approved" && (
          <Typography variant="subtitle2" color="green">
            ✅ You've listed this item
          </Typography>
        )}
        {status === "Invalid" && (
          <Typography variant="subtitle2" color="gray">
            ⚠ This item has expired, it can't be listed
          </Typography>
        )}
      </div>
    );
  }
  if (typeOfNotification === "notifySold") {
    return (
      <Paper
        elevation={0}
        onClick={() => {
          getBuyingHospitalData(trackingMedicineId);
          openPopup(true);
        }}
      >
        Someone has bought your medicine, click here to view detail
      </Paper>
    );
  }
  return (
    <div>
      {medicineName} in your Wish List has just been listed by{" "}
      <b>{getHospitalName()}</b>
      {status === "Init" && (
        <div>
          <Button onClick={() => onDecline({ id })} startIcon={<CloseIcon />}>
            Decline
          </Button>
          <Button onClick={() => onApprove({ id })} startIcon={<CheckIcon />}>
            Buy
          </Button>
        </div>
      )}
      {status === "Declined" && (
        <Typography variant="subtitle2" color="orange">
          ❌ You've declined to buy from this vendor
        </Typography>
      )}
      {status === "Approved" && (
        <Typography variant="subtitle2" color="green">
          🎉 You've bought this item.
        </Typography>
      )}
      {status === "Invalid" && (
        <Typography variant="subtitle2" color="gray">
          ⚠ Someone has purchased this item
        </Typography>
      )}
    </div>
  );
};

NotificationItem.propTypes = {
  medicineName: PropTypes.string,
  hospitalName: PropTypes.string,
  typeOfNotification: PropTypes.string,
  popUpCallbackFunc: PropTypes.func,
  onApproveDecline: PropTypes.func,
};

export default NotificationItem;
