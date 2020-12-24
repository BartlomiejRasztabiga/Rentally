import React from "react";
import { Container, Grid, makeStyles } from "@material-ui/core";
import NewestReservationsListView from "../../reservations/ActiveReservationsListView";
import ActiveRentalsListView from "../../rentals/ActiveRentalsListView";

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: "100%",
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3),
  },
}));

const Dashboard = () => {
  const classes = useStyles();

  return (
    <Container maxWidth={false} className={classes.root}>
      <Grid container spacing={3}>
        <Grid item lg={12}>
          <NewestReservationsListView />
        </Grid>
        <Grid item lg={12}>
          <ActiveRentalsListView />
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
