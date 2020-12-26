import React from "react";
import PropTypes from "prop-types";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import { useParams } from "react-router";
import history from "history/browser";
import CreateUpdateCustomerForm from "../../../components/customers/CreateUpdateCustomerForm";

const useStyles = makeStyles((theme) => ({
  customerDetails: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5),
  },
}));

const CustomerDetails = () => {
  const classes = useStyles();
  let { customerId } = useParams();

  const handleGoBack = () => {
    history.back();
  };

  return (
    <>
      <Container maxWidth={false} className={classes.customerDetails}>
        <Box display="flex" justifyContent="flex-start">
          <Button color="primary" variant="contained" onClick={handleGoBack}>
            Go back
          </Button>
        </Box>
      </Container>
      <Container className={classes.customerDetails}>
        <CreateUpdateCustomerForm customerId={customerId} />
      </Container>
    </>
  );
};

CustomerDetails.propTypes = {
  customerId: PropTypes.number,
};

export default CustomerDetails;
