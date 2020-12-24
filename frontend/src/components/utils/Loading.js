import React from "react";
import { Grid, Typography } from "@material-ui/core";

const Loading = () => {
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
        <Typography variant="h2">Loading...</Typography>
      </Grid>
    </Grid>
  );
};

export default Loading;
