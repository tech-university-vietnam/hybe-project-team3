import { React, useState, useEffect } from "react";
import axios from "axios";
import PropTypes from "prop-types";
import { AppBar, Button, Menu, MenuItem, Toolbar } from "@mui/material";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import Notifications from "components/Notifications/Notifications";

const urlLogOut = "localhost:8000/logout";
const urlGetAllNotifications = "http://localhost:8000/notifications";
const urlGetNotSeenNotifications = "http://localhost:8000/notification/notseen";

const Header = ({ email = "tony_stark@starkindustries.com" }) => {
  const [anchorAccount, setAnchorAccount] = useState(null);
  const [anchorNotification, setAnchorNotification] = useState(null);
  const [notificationBadgeCount, setNotificationBadgeCount] = useState(0);
  const [notifications, setNotifications] = useState([]);

  const openAccount = Boolean(anchorAccount);
  const openNotification = Boolean(anchorNotification);

  console.log("notifications", notifications);

  const handleClickAccount = (event) => {
    setAnchorAccount(event.currentTarget);
  };

  const handleClickNotification = async (event) => {
    setAnchorNotification(event.currentTarget);
    try {
      const response = await axios.get(urlGetAllNotifications, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      setNotifications(response.data);
    } catch (error) {
      console.log("Not able to ");
    }
  };

  const handleClose = () => {
    setAnchorAccount(null);
    setAnchorNotification(null);
  };

  const handleLogout = () => {
    const token = localStorage.getItem("token");
    axios
      .post(urlLogOut, { headers: { Authorization: token } })
      .then((response) => console.log(response))
      .catch((error) => console.log("logout error is", error));
  };

  useEffect(() => {
    let interval = setInterval(async () => {
      try {
        const response = await axios.get(urlGetNotSeenNotifications, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        setNotificationBadgeCount(response.data.length);
      } catch (error) {
        console.log("Cannot call API at interval", error);
      }
    }, 100000);

    return () => {
      clearInterval(interval);
    };
  }, []);

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
          handleClickNotification={handleClickNotification}
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
