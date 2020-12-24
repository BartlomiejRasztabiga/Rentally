import React from "react";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import history from "history/browser";
import { useLocation } from "react-router";
import CreateUpdateRentalForm from "../../../components/rentals/CreateUpdateRentalForm";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
  },
  rentalDetails: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5),
  },
}));

const CreateRentalView = () => {
  const classes = useStyles();
  const location = useLocation();

  const carId = location.state ? location.state.carId : undefined;
  const customerId = location.state ? location.state.customerId : undefined;
  const reservationId = location.state
    ? location.state.reservationId
    : undefined;
  const startDate = location.state ? location.state.startDate : undefined;
  const endDate = location.state ? location.state.endDate : undefined;

  const handleGoBack = () => {
    history.back();
  };

  return (
    <>
      <Container maxWidth={false} className={classes.rentalDetails}>
        <Box display="flex" justifyContent="flex-start">
          <Button color="primary" variant="contained" onClick={handleGoBack}>
            Go back
          </Button>
        </Box>
      </Container>
      <Container className={classes.rentalDetails}>
        <CreateUpdateRentalForm
          carId={carId}
          reservationId={reservationId}
          customerId={customerId}
          startDate={startDate}
          endDate={endDate}
        />
      </Container>
    </>
  );
};

export default CreateRentalView;
