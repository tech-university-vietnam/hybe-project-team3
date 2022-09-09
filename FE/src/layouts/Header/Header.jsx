import { React, useState, useEffect } from "react";
import PropTypes from "prop-types";
import { AppBar, Button, Menu, MenuItem, Toolbar } from "@mui/material";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import useAuth from "../../Utils/hooks/auth.js"
import Notifications from "components/Notifications/Notifications";
import { getNotSeenNotifications, getAllNotifications } from "Utils/api/notification.js";


const Header = ({ email = "tony_stark@starkindustries.com" }) => {
  const [anchorAccount, setAnchorAccount] = useState(null);
  const [anchorNotification, setAnchorNotification] = useState(null);
  const [notificationBadgeCount, setNotificationBadgeCount] = useState(0);
  const [notifications, setNotifications] = useState([]);
  const { logout } = useAuth();

  const openAccount = Boolean(anchorAccount);
  const openNotification = Boolean(anchorNotification);

  const handleClickAccount = (event) => {
    setAnchorAccount(event.currentTarget);
  };

  const handleNotificationDropDownClick = async (event) => {
    setNotificationBadgeCount(0);
    setAnchorNotification(event.currentTarget);
    try {
      const response = await getAllNotifications()
      setNotifications(response.data);
    } catch (error) {
      console.log("Not able to ");
    }
  };

  const handleClose = () => {
    setAnchorAccount(null);
    setAnchorNotification(null);
  };

  const handleLogout = async () => {
    await logout()
      .catch((error) => {
        console.log("logout error is", error);
      });
  };

  useEffect(() => {
    let interval = setInterval(async () => {
      try {
        const response = await getNotSeenNotifications()
        setNotificationBadgeCount(response.data.notseen_noti);
      } catch (error) {
        console.log("Cannot call API at interval", error);
      }
    }, 5000);

    return () => {
      clearInterval(interval);
    };
  }, [notificationBadgeCount]);

  return (
    <AppBar
      position="sticky"
      sx={{
        backgroundColor: "white",
        boxShadow: "none",
        borderBottom: "1px solid #C4C4C4",
      }}
    >
      <Toolbar sx={{ justifyContent: "flex-end" }}>
        <Button
          id="account-button"
          aria-controls={openAccount ? "account-menu" : undefined}
          aria-haspopup="true"
          aria-expanded={openAccount ? "true" : undefined}
          onClick={handleClickAccount}
          variant="text"
          startIcon={<AccountCircleIcon />}
          endIcon={<KeyboardArrowDownIcon />}
          sx={{ color: "black" }}
        >
          {email}
        </Button>
        <Menu
          id="account-menu"
          anchorEl={anchorAccount}
          open={openAccount}
          onClose={handleClose}
          MenuListProps={{
            "aria-labelledby": "account-button",
          }}
        >
          <MenuItem onClick={handleLogout}>Log out</MenuItem>
        </Menu>

        <Notifications
          notifications={notifications}
          notificationBadgeCount={notificationBadgeCount}
          anchorNotification={anchorNotification}
          openNotification={openNotification}
          handleNotificationDropDownClick={handleNotificationDropDownClick}
          handleClose={handleClose}
        />
      </Toolbar>
    </AppBar>
  );
};

Header.propTypes = {
  email: PropTypes.string,
};

export default Header;
