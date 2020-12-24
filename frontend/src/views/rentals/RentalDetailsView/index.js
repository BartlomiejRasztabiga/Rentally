import React from "react";
import PropTypes from "prop-types";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import { useParams } from "react-router";
import history from "history/browser";
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

const RentalDetailsView = () => {
  const classes = useStyles();
  let { rentalId } = useParams();

  const handleGoBack = () => {
    history.back();
  };

  return (
    <React.Fragment>
      <Container maxWidth={false} className={classes.rentalDetails}>
        <Box display="flex" justifyContent="flex-start">
          <Button color="primary" variant="contained" onClick={handleGoBack}>
            Go back
          </Button>
        </Box>
      </Container>
      <Container className={classes.rentalDetails}>
        <CreateUpdateRentalForm rentalId={rentalId} />
      </Container>
    </React.Fragment>
  );
};

RentalDetailsView.propTypes = {
  rentalId: PropTypes.number,
};

export default RentalDetailsView;
