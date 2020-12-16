import React from "react";
import PropTypes from "prop-types";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import { useParams } from "react-router";
import history from "history/browser";
import CreateUpdateCustomerForm from "../../../components/forms/CreateUpdateCustomerForm";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
  },
  link: {
    color: "inherit",
    textDecoration: "none",
  },
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
    <React.Fragment>
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
    </React.Fragment>
  );
};

CustomerDetails.propTypes = {
  className: PropTypes.string,
  customerId: PropTypes.number,
};

export default CustomerDetails;
