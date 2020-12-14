import React from "react";
import PropTypes from "prop-types";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import history from "history/browser";
import CreateUpdateCustomerForm from "../../../components/CreateUpdateCustomerForm";


const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column"
  },
  carDetails: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5)
  }
}));

const CreateCustomerView = () => {
  const classes = useStyles();

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
        <CreateUpdateCustomerForm />
      </Container>
    </React.Fragment>

  );
};

CreateCustomerView.propTypes = {
  className: PropTypes.string
};

export default CreateCustomerView;