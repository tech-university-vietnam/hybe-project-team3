import React from "react";
import PropTypes from "prop-types";
import { Button, Typography, Paper } from "@mui/material";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import axios from "axios";
// status === "init" => render button approve and decline

// status === "declined" => shows a message that user has declined to list item
// when user clicks "Cancel", change status to "Resolved"
// change from "Finished listing" -> "Resolved"

// status === "declined" => shows a message that user has declined to buy from this hospital

// BE checks what type of notification
// if type === "warningExpired" => change status to "Resolved"
// if type === "notifySold" => keep status as available

const urlDecline = "http://localhost:8000/notification/decline";
const urlApprove = "http://localhost:8000/notification/approve";

const NotificationItem = ({
  id,
  medicineName,
  hospitalName,
  typeOfNotification,
  status,
}) => {
  const onDecline = async ({ id }) => {
    try {
      await axios.post(
        urlDecline,
        { id: id },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
    } catch (error) {
      console.log("Error declining notification", error);
    }
  };

  const onApprove = async ({ id }) => {
    try {
      await axios.post(
        urlApprove,
        { id: id },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
    } catch (error) {
      console.log("Error approving notification", error);
    }
  };

  if (typeOfNotification === "warningExpired") {
    return (
      <div>
        {medicineName} in your Tracked List is about to expire!
        {status === "init" && (
          <div>
            <Button onClick={() => onDecline({id})} startIcon={<CloseIcon />}>
              Cancel
            </Button>
            <Button onClick={() => onApprove({id})} startIcon={<CheckIcon />}>
              List
            </Button>
          </div>
        )}
        {status === "declined" && (
          <Typography variant="subtitle2" color="orange">
            ⚠ You've declined to list this item
          </Typography>
        )}
        {status === "approved" && (
          <Typography variant="subtitle2" color="green">
            ✅ You've listed this item
          </Typography>
        )}
      </div>
    );
  }
  if (typeOfNotification === "notifySold") {
    return (
      <Paper elevation={0} onClick={() => onApprove({id})}>
        Someone has bought your medicine, click here to view detail
      </Paper>
    );
  }
  return (
    <div>
      {medicineName} in your Wish List has just been listed by {hospitalName}
      {status === "init" && (
        <div>
          <Button onClick={() => onDecline({id})} startIcon={<CloseIcon />}>
            Decline
          </Button>
          <Button onClick={() => onApprove({id})} startIcon={<CheckIcon />}>
            Buy
          </Button>
        </div>
      )}
      {status === "declined" && (
        <Typography variant="subtitle2" color="orange">
          ⚠ You've declined to buy from this vendor
        </Typography>
      )}
      {status === "approved" && (
        <Typography variant="subtitle2" color="green">
          🎉 You've bought this item. Please wait for {hospitalName} to contact
          you
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
};

export default NotificationItem;
