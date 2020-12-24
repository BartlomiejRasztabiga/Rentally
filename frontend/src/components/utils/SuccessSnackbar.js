import Snackbar from "@material-ui/core/Snackbar";
import Alert from "@material-ui/lab/Alert";
import React from "react";
import PropTypes from "prop-types";

const SuccessSnackbar = ({ successSnackbarOpen, setSuccessSnackbarOpen }) => {
  return (
    <Snackbar
      open={successSnackbarOpen}
      autoHideDuration={3000}
      onClose={() => setSuccessSnackbarOpen(false)}
      anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
    >
      <Alert severity="success">Successfully saved!</Alert>
    </Snackbar>
  );
};

SuccessSnackbar.propTypes = {
  successSnackbarOpen: PropTypes.bool,
  setSuccessSnackbarOpen: PropTypes.func,
};

export default SuccessSnackbar;
