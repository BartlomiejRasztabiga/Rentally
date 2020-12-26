import { Grid, Typography } from "@material-ui/core";
import React from "react";
import PropTypes from "prop-types";

const LoadingError = (loadingError) => {
  return (
    <Grid
      container
      spacing={0}
      direction="column"
      alignItems="center"
      justify="center"
      style={{ minHeight: "100vh" }}
    >
      <Grid item xs={3}>
        <Typography variant="h2">{loadingError}</Typography>
      </Grid>
    </Grid>
  );
};

LoadingError.propTypes = {
  loadingError: PropTypes.string,
};

export default LoadingError;
