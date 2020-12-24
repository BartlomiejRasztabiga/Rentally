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
import Loading from "../Loading";
import { getReservations } from "../../service/reservationsService";

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
import {
  createRental,
  deleteRental,
  getRentalById,
  updateRental,
  updateRentalStatus,
} from "../../service/rentalsService";
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

const COMPLETED = "COMPLETED";

const CreateUpdateRentalForm = ({
  rentalId,
  carId,
  reservationId,
  customerId,
  startDate,
  endDate,
}) => {
  const classes = useStyles();
  const navigate = useNavigate();

  const [rental, setRental] = useState({
    car_id: carId,
    reservation_id: reservationId,
    customer_id: customerId,
    start_date: moment(startDate),
    end_date: moment(endDate),
  });
  const [loaded, setLoaded] = useState(false);
  const [loadingError, setLoadingError] = useState(null);
  const [postError, setPostError] = useState(null);
  const [successSnackbarOpen, setSuccessSnackbarOpen] = useState(false);

  const [availableCars, setAvailableCars] = useState([]);
  const [availableCustomers, setAvailableCustomers] = useState([]);
  const [availableReservations, setAvailableReservations] = useState([]);

  const isInCreateMode = !rentalId;
  const isInEditMode = !isInCreateMode;

  useEffect(() => {
    if (isInEditMode) {
      getRentalById(rentalId)
        .then((_rental) => {
          setRental(_rental);
          setLoadingError(null);
          setLoaded(true);
        })
        .catch((error) => {
          setLoaded(true);
          if (error.response.status === 404) {
            setLoadingError("Rental with given id not found");
          }
        });
    }
  }, [isInEditMode, rentalId]);

  useEffect(() => {
    // get available cars
    getCars().then((cars) => {
      setAvailableCars(cars);
    });

    // get available customers
    getCustomers().then((customers) => {
      setAvailableCustomers(customers);
    });

    // get available reservations
    getReservations().then((reservations) => {
      setAvailableReservations(reservations);
    });
  }, []);

  const emptyIfNull = (value) => {
    return value || "";
  };

  const handleChange = (event) => {
    updateRentalField(event.target.name, event.target.value);
  };

  const handleStartDateChange = (date) => {
    setRental({
      ...rental,
      start_date: date.format(),
    });
  };

  const handleEndDateChange = (date) => {
    setRental({
      ...rental,
      end_date: date.format(),
    });
  };

  const updateRentalField = (fieldName, value) => {
    setRental({
      ...rental,
      [fieldName]: value,
    });
  };

  const handleCreateUpdateRental = () => {
    if (rentalId) {
      handleUpdateRental(rental);
    } else {
      handleCreateRental(rental);
    }
  };

  const handleUpdateRental = (updated_rental) => {
    updateRental(updated_rental)
      .then((_rental) => {
        setRental(_rental);
        setPostError(null);
        setSuccessSnackbarOpen(true);
      })
      .catch((error) => {
        setPostError(JSON.stringify(error.response.data));
      });
  };

  const handleCreateRental = (_rental) => {
    createRental(_rental)
      .then(() => {
        navigate(APP_RENTALS_URL, { replace: true });
      })
      .catch((error) => {
        setPostError(JSON.stringify(error.response.data));
      });
  };

  const handleDeleteRental = () => {
    deleteRental(rentalId).then(() => {
      navigate(APP_RENTALS_URL, { replace: true });
    });
  };

  const handleCompleteRental = () => {
    updateRentalStatus(rental, COMPLETED)
      .then((_rental) => {
        setRental(_rental);
        setPostError(null);
        setSuccessSnackbarOpen(true);
      })
      .catch((error) => {
        setPostError(JSON.stringify(error.response.data));
      });
  };

  if (loadingError) {
    return <LoadingError loadingError={loadingError} />;
  }

  return (
    <React.Fragment>
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
                    <Button
                      variant="outlined"
                      component="span"
                      color="primary"
                      className={classes.changeStatusButton}
                      onClick={handleCompleteRental}
                    >
                      COMPLETE
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
                        value={emptyIfNull(rental.car_id)}
                        onChange={handleChange}
                        label="Car"
                      >
                        {availableCars.map((car, key) => (
                          <MenuItem value={car.id} key={key}>
                            {car.model_name}
                          </MenuItem>
                        ))}
                      </Select>
                      {rental.car_id && (
                        <Button
                          color="primary"
                          endIcon={<ArrowRightIcon />}
                          size="small"
                          variant="text"
                        >
                          <Link
                            className={classes.link}
                            to={`${APP_CARS_URL}/${rental.car_id}`}
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
                        value={emptyIfNull(rental.customer_id)}
                        onChange={handleChange}
                        label="Customer"
                      >
                        {availableCustomers.map((customer, key) => (
                          <MenuItem value={customer.id} key={key}>
                            {customer.full_name}
                          </MenuItem>
                        ))}
                      </Select>
                      {rental.customer_id && (
                        <Button
                          color="primary"
                          endIcon={<ArrowRightIcon />}
                          size="small"
                          variant="text"
                        >
                          <Link
                            className={classes.link}
                            to={`${APP_CUSTOMERS_URL}/${rental.customer_id}`}
                          >
                            Go to
                          </Link>
                        </Button>
                      )}
                    </FormControl>
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>Reservation (optional)</InputLabel>
                      <Select
                        name="reservation_id"
                        value={emptyIfNull(rental.reservation_id)}
                        onChange={handleChange}
                        label="Reservation"
                      >
                        <MenuItem value={null}>EMPTY</MenuItem>
                        {availableReservations.map((reservation, key) => (
                          <MenuItem value={reservation.id} key={key}>
                            {reservation.id}
                          </MenuItem>
                        ))}
                      </Select>
                      {rental.reservation_id && (
                        <Button
                          color="primary"
                          endIcon={<ArrowRightIcon />}
                          size="small"
                          variant="text"
                        >
                          <Link
                            className={classes.link}
                            to={`${APP_RESERVATIONS_URL}/${rental.reservation_id}`}
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
                      value={rental.start_date}
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
                      value={rental.end_date}
                    />
                  </Grid>
                  {/* new rental always starts with NEW status */}
                  {isInEditMode && (
                    <Grid item md={6} xs={12}>
                      <TextField
                        fullWidth
                        label="Status"
                        name="status"
                        value={emptyIfNull(rental.status)}
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
                    onClick={handleCreateUpdateRental}
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
                        onClick={handleDeleteRental}
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

CreateUpdateRentalForm.propTypes = {
  className: PropTypes.string,
  rentalId: PropTypes.string,
  carId: PropTypes.number,
  reservationId: PropTypes.number,
  customerId: PropTypes.number,
  startDate: PropTypes.instanceOf(Date),
  endDate: PropTypes.instanceOf(Date),
};

export default CreateUpdateRentalForm;
