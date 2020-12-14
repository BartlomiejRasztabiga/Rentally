import React from "react";
import PropTypes from "prop-types";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import { useParams } from "react-router";
import history from "history/browser";
import CreateUpdateCustomerForm from "../../../components/CreateUpdateCustomerForm";


const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column"
  },
  link: {
    color: "inherit",
    textDecoration: "none"
  },
  carDetails: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5)
  },
  uploadImageBox: {
    alignItems: "center",
    justifyContent: "center"
  }
}));

const CustomerDetails = () => {
  const classes = useStyles();
  let { customerId } = useParams();

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
        <CreateUpdateCustomerForm customerId={customerId} />
      </Container>
    </React.Fragment>

  );
};

CustomerDetails.propTypes = {
  className: PropTypes.string,
  customerId: PropTypes.number
};

export default CustomerDetails;