import React from "react";
import PropTypes from "prop-types";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import { useParams } from "react-router";
import history from "history/browser";
import CreateUpdateCarForm from "../../../components/cars/CreateUpdateCarForm";

const useStyles = makeStyles((theme) => ({
  carDetails: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5),
  },
}));

const CarDetails = () => {
  const classes = useStyles();
  let { carId } = useParams();

  const handleGoBack = () => {
    history.back();
  };

  return (
    <React.Fragment>
      <Container maxWidth={false} className={classes.carDetails}>
        <Box display="flex" justifyContent="flex-start">
          <Button color="primary" variant="contained" onClick={handleGoBack}>
            Go back
          </Button>
        </Box>
      </Container>
      <Container className={classes.carDetails}>
        <CreateUpdateCarForm carId={carId} />
      </Container>
    </React.Fragment>
  );
};

CarDetails.propTypes = {
  carId: PropTypes.number,
};

export default CarDetails;
