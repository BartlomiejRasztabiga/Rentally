import ReactJson from "react-json-view";
import React from "react";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  errorBox: {
    margin: theme.spacing(5),
  },
}));

const ErrorBox = (error) => {
  const classes = useStyles();

  return (
    <div color="error" className={classes.errorBox}>
      <ReactJson src={error.error} theme="ocean" />
    </div>
  );
};

ErrorBox.propTypes = {
  error: PropTypes.string,
};

export default ErrorBox;
