import React from "react";
import { Link as RouterLink } from "react-router-dom";
import clsx from "clsx";
import PropTypes from "prop-types";
import {
  AppBar,
  Box,
  IconButton,
  makeStyles,
  Toolbar,
} from "@material-ui/core";
import InputIcon from "@material-ui/icons/Input";
import Logo from "../../components/Logo";
import { useAuth } from "../../context/auth";

const useStyles = makeStyles(() => ({
  root: {},
}));

const TopBar = ({ className, ...rest }) => {
  const classes = useStyles();
  const { setAccessToken } = useAuth();

  const logout = () => {
    setAccessToken(null);
  };

  return (
    <AppBar className={clsx(classes.root, className)} elevation={0} {...rest}>
      <Toolbar>
        <RouterLink to="/">
          <Logo />
        </RouterLink>
        <Box flexGrow={1} />
        <IconButton color="inherit" onClick={logout}>
          <InputIcon />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

TopBar.propTypes = {
  className: PropTypes.string,
};

export default TopBar;
