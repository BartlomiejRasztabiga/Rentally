import React from "react";
import {
  Avatar,
  Box,
  Divider,
  Drawer,
  List,
  makeStyles,
  Typography,
} from "@material-ui/core";
import DriveEtaIcon from "@material-ui/icons/DriveEta";
import SupervisorAccountIcon from "@material-ui/icons/SupervisorAccount";
import DashboardIcon from "@material-ui/icons/Dashboard";
import AssignmentIcon from "@material-ui/icons/Assignment";
import LocalAtmIcon from "@material-ui/icons/LocalAtm";
import MoneyOffIcon from "@material-ui/icons/MoneyOff";

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
    href: `${APP_RENTALS_URL}/overtime`,
    icon: MoneyOffIcon,
    title: "Overtime Rentals",
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
  desktopDrawer: {
    width: 256,
    top: 64,
    height: "calc(100% - 64px)",
  },
  avatar: {
    width: 64,
    height: 64,
  },
}));

const NavBar = () => {
  const classes = useStyles();

  const content = (
    <Box height="100%" display="flex" flexDirection="column">
      <Box alignItems="center" display="flex" flexDirection="column" p={2}>
        <Avatar className={classes.avatar} src={user.avatar} />
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
    <Drawer
      anchor="left"
      classes={{ paper: classes.desktopDrawer }}
      open
      variant="persistent"
    >
      {content}
    </Drawer>
  );
};

export default NavBar;
