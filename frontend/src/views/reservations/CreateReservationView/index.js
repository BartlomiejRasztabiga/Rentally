import React from "react";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import history from "history/browser";
import CreateUpdateReservationForm from "../../../components/reservations/CreateUpdateReservationForm";
import { useLocation } from "react-router";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
  },
  reservationDetails: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5),
  },
}));

const CreateReservationView = () => {
  const classes = useStyles();
  const location = useLocation();

  const carId = location.state ? location.state.carId : undefined;

  const handleGoBack = () => {
    history.back();
  };

  return (
    <React.Fragment>
      <Container maxWidth={false} className={classes.reservationDetails}>
        <Box display="flex" justifyContent="flex-start">
          <Button color="primary" variant="contained" onClick={handleGoBack}>
            Go back
          </Button>
        </Box>
      </Container>
      <Container className={classes.reservationDetails}>
        <CreateUpdateReservationForm carId={carId} />
      </Container>
    </React.Fragment>
  );
};

export default CreateReservationView;
