import { React, useState } from "react";
import axios from "axios";
import PropTypes from "prop-types";
import {
  AppBar,
  Button,
  Badge,
  IconButton,
  Menu,
  MenuItem,
  Toolbar,
} from "@mui/material";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import NotificationsIcon from "@mui/icons-material/Notifications";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

const Header = (props) => {
  const [anchorAccount, setAnchorAccount] = useState(null);
  const [anchorNotification, setAnchorNotification] = useState(null);
  const [notifications, setNotifications] = useState([1, 2, 3]);

  const openAccount = Boolean(anchorAccount);
  const openNotification = Boolean(anchorNotification);

  const handleClickAccount = (event) => {
    setAnchorAccount(event.currentTarget);
  };

  const handleClickNotification = (event) => {
    setAnchorNotification(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorAccount(null);
    setAnchorNotification(null);
  };

  const handleLogout = () => {};

  return (
    <AppBar
      position="sticky"
      sx={{
        backgroundColor: "white",
        boxShadow: "none",
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
          Tony Stark
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

        <IconButton
          id="notification-button"
          aria-controls={anchorNotification ? "notification-menu" : undefined}
          aria-haspopup="true"
          aria-expanded={anchorNotification ? "true" : undefined}
          onClick={handleClickNotification}
        >
          <Badge badgeContent={5} color="error">
            <NotificationsIcon />
          </Badge>
        </IconButton>
        <Menu
          id="notification-menu"
          anchorEl={anchorNotification}
          open={anchorNotification}
          onClose={handleClose}
          MenuListProps={{
            "aria-labelledby": "notification-button",
          }}
        >
          {notifications.map((notification) => (
            <MenuItem>Notification</MenuItem>
          ))}
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

Header.propTypes = {};

export default Header;
