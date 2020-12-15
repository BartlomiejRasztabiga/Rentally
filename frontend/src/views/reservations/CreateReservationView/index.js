import React from "react";
import PropTypes from "prop-types";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import history from "history/browser";
import CreateUpdateReservationForm from "../../../components/CreateUpdateReservationForm";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column"
  },
  reservationDetails: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5)
  }
}));

const CreateReservationView = () => {
  const classes = useStyles();

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
        <CreateUpdateReservationForm />
      </Container>
    </React.Fragment>
  );
};

CreateReservationView.propTypes = {
  className: PropTypes.string
};

export default CreateReservationView;
