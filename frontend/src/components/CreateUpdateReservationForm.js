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
import Loading from "./Loading";
import ReactJson from "react-json-view";
import Snackbar from "@material-ui/core/Snackbar";
import Alert from "@material-ui/lab/Alert";
import {
  createReservation,
  deleteReservation,
  getReservationById,
  updateReservation,
  updateReservationStatus,
} from "../service/reservationsService";

import { APP_RESERVATIONS_URL } from "../config";
import { DateTimePicker } from "@material-ui/pickers";
import moment from "moment";
import { getCars } from "../service/carsService";
import { getCustomers } from "../service/customersService";
import Select from "@material-ui/core/Select";
import InputLabel from "@material-ui/core/InputLabel";
import FormControl from "@material-ui/core/FormControl";
import MenuItem from "@material-ui/core/MenuItem";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
  },
  link: {
    color: "inherit",
    textDecoration: "none",
  },
  reservationDetails: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5),
  },
  errorBox: {
    margin: theme.spacing(5),
  },
  changeStatusButtonsBox: {
    marginTop: theme.spacing(3),
    marginBottom: theme.spacing(3),
  },
  changeStatusButton: {
    margin: theme.spacing(1),
  },
}));

const COLLECTED = "COLLECTED";
const CANCELLED = "CANCELLED";

const CreateUpdateReservationForm = ({ reservationId }) => {
  const classes = useStyles();
  const navigate = useNavigate();

  const [reservation, setReservation] = useState({
    start_date: moment(),
    end_date: moment().add(1, 'days'),
  });
  const [loaded, setLoaded] = useState(false);
  const [loadingError, setLoadingError] = useState(null);
  const [postError, setPostError] = useState(null);
  const [successSnackbarOpen, setSuccessSnackbarOpen] = useState(false);

  const [availableCars, setAvailableCars] = useState([]);
  const [availableCustomers, setAvailableCustomers] = useState([]);

  const isInCreateMode = !reservationId;
  const isInEditMode = !isInCreateMode;

  useEffect(() => {
    if (isInEditMode) {
      getReservationById(reservationId)
        .then((reservation) => {
          setReservation(reservation);
          setLoadingError(null);
          setLoaded(true);
        })
        .catch((error) => {
          setLoaded(true);
          if (error.response.status === 404) {
            setLoadingError("Reservation with given id not found");
          }
        });
    }
  }, [isInEditMode, reservationId]);

  useEffect(() => {
    // get available cars
    getCars().then((cars) => {
      setAvailableCars(cars);
    });

    // get available customers
    getCustomers().then((customers) => {
      setAvailableCustomers(customers);
    });
  }, []);

  const emptyIfNull = (value) => {
    return value || "";
  };

  const handleChange = (event) => {
    updateReservationField(event.target.name, event.target.value);
  };

  const handleStartDateChange = (date) => {
    setReservation({
      ...reservation,
      start_date: date.format(),
    });
  };

  const handleEndDateChange = (date) => {
    setReservation({
      ...reservation,
      end_date: date.format(),
    });
  };

  const updateReservationField = (fieldName, value) => {
    setReservation({
      ...reservation,
      [fieldName]: value,
    });
  };

  const handleCreateUpdateReservation = () => {
    if (reservationId) {
      handleUpdateReservation(reservation);
    } else {
      handleCreateReservation(reservation);
    }
  };

  const handleUpdateReservation = (reservation) => {
    updateReservation(reservation)
      .then((reservation) => {
        setReservation(reservation);
        setPostError(null);
        setSuccessSnackbarOpen(true);
      })
      .catch((error) => {
        setPostError(JSON.stringify(error.response.data));
      });
  };

  const handleCreateReservation = (reservation) => {
    createReservation(reservation)
      .then((reservation) => {
        navigate(APP_RESERVATIONS_URL, { replace: true });
      })
      .catch((error) => {
        setPostError(JSON.stringify(error.response.data));
      });
  };

  const handleDeleteReservation = () => {
    deleteReservation(reservationId).then(() => {
      navigate(APP_RESERVATIONS_URL, { replace: true });
    });
  };

  const handleCollectReservation = () => {
    updateReservationStatus(reservation, COLLECTED)
      .then(() => {
        setReservation(reservation);
        setPostError(null);
        setSuccessSnackbarOpen(true);
      })
      .catch((error) => {
        setPostError(JSON.stringify(error.response.data));
      });
  };

  const handleCancelReservation = () => {
    updateReservationStatus(reservation, CANCELLED)
      .then(() => {
        navigate(APP_RESERVATIONS_URL, { replace: true });
      })
      .catch((error) => {
        setPostError(JSON.stringify(error.response.data));
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
              {isInEditMode && (
                <Grid
                  container
                  className={classes.changeStatusButtonsBox}
                  justify="flex-end"
                >
                  <Grid item md={3}>
                    <Button
                      variant="outlined"
                      component="span"
                      color="primary"
                      className={classes.changeStatusButton}
                      onClick={handleCollectReservation}
                    >
                      COLLLECT
                    </Button>
                    <Button
                      variant="outlined"
                      component="span"
                      color="secondary"
                      className={classes.changeStatusButton}
                      onClick={handleCancelReservation}
                    >
                      CANCEL
                    </Button>
                  </Grid>
                </Grid>
              )}
              <form autoComplete="off">
                <Grid container spacing={3}>
                  <Grid item md={6} xs={12}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>Car</InputLabel>
                      <Select
                        name="car_id"
                        value={emptyIfNull(reservation.car_id)}
                        onChange={handleChange}
                        label="Car"
                      >
                        {availableCars.map((car, key) => (
                          <MenuItem value={car.id} key={key}>
                            {car.model_name}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>Customer</InputLabel>
                      <Select
                        name="customer_id"
                        value={emptyIfNull(reservation.customer_id)}
                        onChange={handleChange}
                        label="Customer"
                      >
                        {availableCustomers.map((customer, key) => (
                          <MenuItem value={customer.id} key={key}>
                            {customer.full_name}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <DateTimePicker
                      fullWidth
                      ampm={false}
                      label="Start date"
                      name="start_date"
                      inputVariant="outlined"
                      disablePast={isInCreateMode}
                      onChange={handleStartDateChange}
                      value={reservation.start_date}
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <DateTimePicker
                      fullWidth
                      ampm={false}
                      label="End date"
                      name="end_date"
                      inputVariant="outlined"
                      disablePast={isInCreateMode}
                      onChange={handleEndDateChange}
                      value={reservation.end_date}
                    />
                  </Grid>
                  {/* new reservation always starts with NEW status */}
                  {isInEditMode && (
                    <Grid item md={6} xs={12}>
                      <TextField
                        fullWidth
                        label="Status"
                        name="status"
                        value={emptyIfNull(reservation.status)}
                        variant="outlined"
                        disabled
                      />
                    </Grid>
                  )}
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
                    onClick={handleCreateUpdateReservation}
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
                        onClick={handleDeleteReservation}
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

CreateUpdateReservationForm.propTypes = {
  className: PropTypes.string,
  reservationId: PropTypes.string,
};

export default CreateUpdateReservationForm;
