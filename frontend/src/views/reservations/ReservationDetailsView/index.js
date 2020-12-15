import React from "react";
import PropTypes from "prop-types";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import { useParams } from "react-router";
import history from "history/browser";
import CreateUpdateReservationForm from "../../../components/CreateUpdateReservationForm";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column"
  },
  link: {
    color: "inherit",
    textDecoration: "none"
  },
  reservationDetails: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5)
  }
}));

const ReservationDetails = () => {
  const classes = useStyles();
  let { reservationId } = useParams();

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
        <CreateUpdateReservationForm reservationId={reservationId} />
      </Container>
    </React.Fragment>
  );
};

ReservationDetails.propTypes = {
  className: PropTypes.string,
  reservationId: PropTypes.number
};

export default ReservationDetails;
