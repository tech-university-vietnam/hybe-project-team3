import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import NotificationItem from "components/NotificationItem/NotificationItem";
import { Badge, Button, IconButton, Menu, MenuItem } from "@mui/material";
import NotificationsIcon from "@mui/icons-material/Notifications";

// This component will render out a list of NotificationItem component
// This component will call the API at a set interval to get updates on any new
// notification from the BE

// **trackedListNotification**:
// warningExpired
// 1. medicineName in your tracked list is about to expire, click here to list it!
// notifySold
// *2a. someone has bought your medicine, click here to view the contact info

// **wishListNotification**:
// notifyAvailable
// *1c. medicine A in your WishList has just been listed by hospital X
const numberOfNotificationToShow = 3;

const Notifications = ({
  notifications,
  notificationBadgeCount,
  anchorNotification,
  openNotification,
  handleNotificationDropDownClick,
  handleClose,
  onApproveDecline,
  openPopup,
  getBuyingHospitalData,
}) => {
  console.log("notifications", notifications);
  const [next, setNext] = useState(numberOfNotificationToShow);
  const handleMoreNotifications = () => {
    setNext(next + numberOfNotificationToShow);
  };
  return (
    <div>
      <IconButton
        id="notification-button"
        aria-controls={anchorNotification ? "notification-menu" : undefined}
        aria-haspopup="true"
        aria-expanded={anchorNotification ? "true" : undefined}
        onClick={handleNotificationDropDownClick}
      >
        <Badge badgeContent={notificationBadgeCount} color="error">
          <NotificationsIcon />
        </Badge>
      </IconButton>
      <Menu
        id="notification-menu"
        anchorEl={anchorNotification}
        open={openNotification}
        onClose={handleClose}
        PaperProps={{
          style: {
            maxHeight: 450,
          },
        }}
        MenuListProps={{
          "aria-labelledby": "notification-button",
        }}
      >
        {notifications
          .slice(0, next)
          .map(
            ({
              id,
              tracking_medicine_id: trackingMedicineId,
              sourcing_id: sourcingId,
              type,
              from_hospital: fromHospital,
              to_hospital: toHospital,
              sourcing_name: medicineName,
              status,
            }) => (
              <MenuItem key={id} divider sx={{ height: "70px" }}>
                <NotificationItem
                  id={id}
                  sourcingId={sourcingId}
                  trackingMedicineId={trackingMedicineId}
                  typeOfNotification={type}
                  status={status}
                  fromHospital={fromHospital}
                  toHospital={toHospital}
                  medicineName={medicineName}
                  onApproveDecline={onApproveDecline}
                  openPopup={openPopup}
                  getBuyingHospitalData={getBuyingHospitalData}
                />
              </MenuItem>
            )
          )}
        <Button
          className="mt-4"
          onClick={handleMoreNotifications}
          disabled={next >= notifications.length ? true : false}
        >
          Load more
        </Button>
      </Menu>
    </div>
  );
};

Notifications.propTypes = {
  anchorNotification: PropTypes.object,
  openNotification: PropTypes.bool,
  handleNotificationDropDownClick: PropTypes.func,
  handleClose: PropTypes.func,
  onApproveDecline: PropTypes.func,
  openPopup: PropTypes.func,
};

export default Notifications;
