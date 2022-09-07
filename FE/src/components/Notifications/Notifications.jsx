import React from "react";
import axios from "axios";
import PropTypes from "prop-types";
import NotificationItem from "components/NotificationItem/NotificationItem";

// This component will render out a list of NotificationItem component
// This component will call the API at a set interval to get updates on any new
// notification from the BE

// 2 types of notifications:
// - Notification for near-expired medicines (trackedListNotification)
// - Notification for medicine in wishlist becomes available (wishListNotification)

// trackedListNotification:
// medicineName in your tracked list is about to expire, click here to list it!

// wishListNotification:
// medicineName in your WishList has just become available!

// NEED TO KNOW:
// - what will the information from BE looks like for the 2 types of notifications

const Notifications = (props) => {
  // call BE to get the list of notifications
  // .map over the array of notifications, for each element render the <NotificationItem />
  // and pass it the type of notification and medicineName

  const getNotifications = async () => {
    try {
      await axios.get();
    } catch (error) {
      console.log("Error getting list of notifications", error);
    }
  };
  return (
    <div>
      Notifications
      <NotificationItem />
    </div>
  );
};

Notifications.propTypes = {};

export default Notifications;
