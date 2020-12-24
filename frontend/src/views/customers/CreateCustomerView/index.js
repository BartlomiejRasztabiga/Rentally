import React from "react";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import history from "history/browser";
import CreateUpdateCustomerForm from "../../../components/customers/CreateUpdateCustomerForm";

const useStyles = makeStyles((theme) => ({
  carDetails: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5),
  },
}));

const CreateCustomerView = () => {
  const classes = useStyles();

  const handleGoBack = () => {
    history.back();
  };

  return (
    <>
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
    </>
  );
};

export default CreateCustomerView;
