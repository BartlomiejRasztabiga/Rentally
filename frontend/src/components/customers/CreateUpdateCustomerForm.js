import React, { useEffect, useState } from "react";
import {
  Button,
  Card,
  CardActions,
  CardContent,
  Container,
  Grid,
  makeStyles,
  TextField,
  Typography,
} from "@material-ui/core";
import clsx from "clsx";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import Loading from "../Loading";
import ReactJson from "react-json-view";
import {
  createCustomer,
  deleteCustomer,
  getCustomerById,
  updateCustomer,
} from "../../service/customersService";
import { APP_CUSTOMERS_URL } from "../../config";
import Snackbar from "@material-ui/core/Snackbar";
import Alert from "@material-ui/lab/Alert";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
  },
  customerDetails: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5),
  },
  errorBox: {
    margin: theme.spacing(5),
  },
}));

const CreateUpdateCustomerForm = ({ customerId }) => {
  const classes = useStyles();
  const navigate = useNavigate();

  const [customer, setCustomer] = useState({});
  const [loaded, setLoaded] = useState(false);
  const [loadingError, setLoadingError] = useState(null);
  const [postError, setPostError] = useState(null);
  const [successSnackbarOpen, setSuccessSnackbarOpen] = useState(false);

  const isInCreateMode = !customerId;
  const isInEditMode = !isInCreateMode;

  useEffect(() => {
    if (isInEditMode) {
      getCustomerById(customerId)
        .then((_customer) => {
          setCustomer(_customer);
          setLoadingError(null);
          setLoaded(true);
        })
        .catch((error) => {
          setLoaded(true);
          if (error.response.status === 404) {
            setLoadingError("Customer with given id not found");
          }
        });
    }
  }, [isInEditMode, customerId]);

  const emptyIfNull = (value) => {
    return value || "";
  };

  const handleChange = (event) => {
    updateCustomerField(event.target.name, event.target.value);
  };

  const updateCustomerField = (fieldName, value) => {
    setCustomer({
      ...customer,
      [fieldName]: value,
    });
  };

  const handleCreateUpdateCustomer = () => {
    if (customerId) {
      handleUpdateCustomer(customer);
    } else {
      handleCreateCustomer(customer);
    }
  };

  const handleUpdateCustomer = (updated_customer) => {
    updateCustomer(updated_customer)
      .then((_customer) => {
        setCustomer(_customer);
        setPostError(null);
        setSuccessSnackbarOpen(true);
      })
      .catch((error) => {
        setPostError(JSON.stringify(error.response.data));
      });
  };

  const handleCreateCustomer = (_customer) => {
    createCustomer(_customer)
      .then(() => {
        navigate(APP_CUSTOMERS_URL, { replace: true });
      })
      .catch((error) => {
        setPostError(JSON.stringify(error.response.data));
      });
  };

  const handleDeleteCustomer = () => {
    deleteCustomer(customerId).then(() => {
      navigate(APP_CUSTOMERS_URL, { replace: true });
    });
  };

  if (loadingError) {
    return (
      <Grid
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justify="center"
        style={{ minHeight: "100vh" }}
      >
        <Grid item xs={3}>
          <Typography variant="h2">{loadingError}</Typography>
        </Grid>
      </Grid>
    );
  }

  return (
    <React.Fragment>
      {loaded || isInCreateMode ? (
        <Container className={classes.customerDetails}>
          {/*TODO Can extract snackbar to another component? */}
          <Snackbar
            open={successSnackbarOpen}
            autoHideDuration={3000}
            onClose={() => setSuccessSnackbarOpen(false)}
            anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
          >
            <Alert severity="success">Successfully saved!</Alert>
          </Snackbar>
          <Card className={clsx(classes.root)}>
            <CardContent>
              {postError && (
                <div color="error" className={classes.errorBox}>
                  <ReactJson src={JSON.parse(postError)} theme="ocean" />
                </div>
              )}
              <form autoComplete="off">
                <Grid container spacing={3}>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Full name"
                      name="full_name"
                      onChange={handleChange}
                      required
                      error={!customer.full_name}
                      value={emptyIfNull(customer.full_name)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Address"
                      name="address"
                      onChange={handleChange}
                      value={emptyIfNull(customer.address)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Phone number"
                      name="phone_number"
                      onChange={handleChange}
                      value={emptyIfNull(customer.phone_number)}
                      variant="outlined"
                    />
                  </Grid>
                </Grid>
              </form>
            </CardContent>
            <CardActions disableSpacing>
              <Grid container>
                <Grid item md={6}>
                  <Button
                    variant="contained"
                    component="span"
                    color="primary"
                    onClick={handleCreateUpdateCustomer}
                  >
                    Save
                  </Button>
                </Grid>
                {isInEditMode && (
                  <Grid item md={6}>
                    <Grid container justify="flex-end">
                      <Button
                        variant="contained"
                        component="span"
                        color="secondary"
                        onClick={handleDeleteCustomer}
                      >
                        Delete
                      </Button>
                    </Grid>
                  </Grid>
                )}
              </Grid>
            </CardActions>
          </Card>
        </Container>
      ) : (
        <Loading />
      )}
    </React.Fragment>
  );
};

CreateUpdateCustomerForm.propTypes = {
  className: PropTypes.string,
  carId: PropTypes.string,
};

export default CreateUpdateCustomerForm;
