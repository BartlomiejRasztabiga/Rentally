import React, { useEffect } from "react";
import { Link as RouterLink, useLocation } from "react-router-dom";
import PropTypes from "prop-types";
import {
  Avatar,
  Box,
  Divider,
  Drawer,
  Hidden,
  List,
  makeStyles,
  Typography,
} from "@material-ui/core";
import DriveEtaIcon from "@material-ui/icons/DriveEta";
import SupervisorAccountIcon from "@material-ui/icons/SupervisorAccount";
import DashboardIcon from "@material-ui/icons/Dashboard";
import AssignmentIcon from "@material-ui/icons/Assignment";
import LocalAtmIcon from "@material-ui/icons/LocalAtm";

import NavItem from "./NavItem";
import {
  APP_CARS_URL,
  APP_CUSTOMERS_URL,
  APP_RENTALS_URL,
  APP_RESERVATIONS_URL,
} from "../../../config";

const user = {
  avatar: "/static/images/avatars/avatar_1.jpeg",
  name: "Test Employee",
};

const items = [
  {
    href: "/app/dashboard",
    icon: DashboardIcon,
    title: "Dashboard",
  },
  {
    href: APP_RESERVATIONS_URL,
    icon: AssignmentIcon,
    title: "Reservations",
  },
  {
    href: APP_RENTALS_URL,
    icon: LocalAtmIcon,
    title: "Rentals",
  },
  {
    href: APP_CUSTOMERS_URL,
    icon: SupervisorAccountIcon,
    title: "Customers",
  },
  {
    href: APP_CARS_URL,
    icon: DriveEtaIcon,
    title: "Cars",
  },
];

const useStyles = makeStyles(() => ({
  mobileDrawer: {
    width: 256,
  },
  desktopDrawer: {
    width: 256,
    top: 64,
    height: "calc(100% - 64px)",
  },
  avatar: {
    cursor: "pointer",
    width: 64,
    height: 64,
  },
}));

const NavBar = ({ onMobileClose, openMobile }) => {
  const classes = useStyles();
  const location = useLocation();

  useEffect(() => {
    if (openMobile && onMobileClose) {
      onMobileClose();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.pathname]);

  const content = (
    <Box height="100%" display="flex" flexDirection="column">
      <Box alignItems="center" display="flex" flexDirection="column" p={2}>
        <Avatar
          className={classes.avatar}
          component={RouterLink}
          src={user.avatar}
          to="/app/account"
        />
        <Typography className={classes.name} color="textPrimary" variant="h5">
          {user.name}
        </Typography>
      </Box>
      <Divider />
      <Box p={2}>
        <List>
          {items.map((item) => (
            <NavItem
              href={item.href}
              key={item.title}
              title={item.title}
              icon={item.icon}
            />
          ))}
        </List>
      </Box>
      <Box flexGrow={1} />
    </Box>
  );

  return (
    <>
      <Hidden lgUp>
        <Drawer
          anchor="left"
          classes={{ paper: classes.mobileDrawer }}
          onClose={onMobileClose}
          open={openMobile}
          variant="temporary"
        >
          {content}
        </Drawer>
      </Hidden>
      <Hidden mdDown>
        <Drawer
          anchor="left"
          classes={{ paper: classes.desktopDrawer }}
          open
          variant="persistent"
        >
          {content}
        </Drawer>
      </Hidden>
    </>
  );
};

NavBar.propTypes = {
  onMobileClose: PropTypes.func,
  openMobile: PropTypes.bool,
};

NavBar.defaultProps = {
  onMobileClose: () => {},
  openMobile: false,
};

export default NavBar;
