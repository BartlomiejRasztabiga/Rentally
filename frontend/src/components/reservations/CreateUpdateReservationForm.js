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
} from "@material-ui/core";
import clsx from "clsx";
import { Link, useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import Loading from "../utils/Loading";
import {
  createReservation,
  deleteReservation,
  getReservationById,
  updateReservation,
  updateReservationStatus,
} from "../../service/reservationsService";

import {
  APP_CARS_URL,
  APP_CUSTOMERS_URL,
  APP_RENTALS_URL,
  APP_RESERVATIONS_URL,
} from "../../config";
import { DateTimePicker } from "@material-ui/pickers";
import moment from "moment";
import { getCars } from "../../service/carsService";
import { getCustomers } from "../../service/customersService";
import Select from "@material-ui/core/Select";
import InputLabel from "@material-ui/core/InputLabel";
import FormControl from "@material-ui/core/FormControl";
import MenuItem from "@material-ui/core/MenuItem";
import ArrowRightIcon from "@material-ui/icons/ArrowRight";
import ErrorBox from "../utils/ErrorBox";
import SuccessSnackbar from "../utils/SuccessSnackbar";
import LoadingError from "../utils/LoadingError";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
  },
  link: {
    color: "inherit",
    textDecoration: "none",
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

const CANCELLED = "CANCELLED";

const CreateUpdateReservationForm = ({ reservationId, carId }) => {
  const classes = useStyles();
  const navigate = useNavigate();

  const [reservation, setReservation] = useState({
    car_id: carId,
    start_date: moment(),
    end_date: moment().add(1, "days"),
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
        .then((_reservation) => {
          setReservation(_reservation);
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
    getCars().then((cars) => {
      setAvailableCars(cars);
    });

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

  const handleUpdateReservation = (updated_reservation) => {
    updateReservation(updated_reservation)
      .then((_reservation) => {
        setReservation(_reservation);
        setPostError(null);
        setSuccessSnackbarOpen(true);
      })
      .catch((error) => {
        setPostError(JSON.stringify(error.response.data));
      });
  };

  const handleCreateReservation = (_reservation) => {
    createReservation(_reservation)
      .then(() => {
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
    navigate(`${APP_RENTALS_URL}/new`, {
      replace: true,
      state: {
        reservationId: reservation.id,
        carId: reservation.car_id,
        customerId: reservation.customer_id,
        startDate: reservation.start_date,
        endDate: reservation.end_date,
      },
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
    return <LoadingError loadingError={loadingError} />;
  }

  return (
    <>
      {loaded || isInCreateMode ? (
        <Container className={classes.customerDetails}>
          <SuccessSnackbar
            successSnackbarOpen={successSnackbarOpen}
            setSuccessSnackbarOpen={setSuccessSnackbarOpen}
          />
          <Card className={clsx(classes.root)}>
            <CardContent>
              {postError && <ErrorBox error={JSON.parse(postError)} />}
              {isInEditMode && (
                <Grid
                  container
                  className={classes.changeStatusButtonsBox}
                  justify="flex-end"
                >
                  <Grid item md={3}>
                    {reservation.status === "NEW" && (
                      <Button
                        variant="outlined"
                        component="span"
                        color="primary"
                        className={classes.changeStatusButton}
                        onClick={handleCollectReservation}
                      >
                        COLLLECT (Convert to Rental)
                      </Button>
                    )}
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
                      {reservation.car_id && (
                        <Button
                          color="primary"
                          endIcon={<ArrowRightIcon />}
                          size="small"
                          variant="text"
                        >
                          <Link
                            className={classes.link}
                            to={`${APP_CARS_URL}/${reservation.car_id}`}
                          >
                            Go to
                          </Link>
                        </Button>
                      )}
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
                      {reservation.customer_id && (
                        <Button
                          color="primary"
                          endIcon={<ArrowRightIcon />}
                          size="small"
                          variant="text"
                        >
                          <Link
                            className={classes.link}
                            to={`${APP_CUSTOMERS_URL}/${reservation.customer_id}`}
                          >
                            Go to
                          </Link>
                        </Button>
                      )}
                    </FormControl>
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <DateTimePicker
                      fullWidth
                      showTodayButton
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
                      showTodayButton
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
    </>
  );
};

CreateUpdateReservationForm.propTypes = {
  className: PropTypes.string,
  reservationId: PropTypes.string,
};

export default CreateUpdateReservationForm;
