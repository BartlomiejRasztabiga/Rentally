import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Container,
  FormControl,
  Grid,
  InputLabel,
  makeStyles,
  MenuItem,
  Paper,
  Select,
  TextField,
  Typography
} from "@material-ui/core";
import clsx from "clsx";
import { useNavigate } from "react-router-dom";
import PropTypes from "prop-types";
import { createCar, deleteCar, getCarById, updateCar } from "../service/carsService";
import convertToBase64 from "../utils/convertToBase64";
import Loading from "./Loading";
import ReactJson from "react-json-view";


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
  },
  errorBox: {
    margin: theme.spacing(5)
  }
}));

const CreateUpdateCarForm = ({ carId }) => {
  const classes = useStyles();
  const navigate = useNavigate();

  const [car, setCar] = useState({});
  const [loaded, setLoaded] = useState(false);
  const [loadingError, setLoadingError] = useState(null);
  const [postError, setPostError] = useState(null);

  const isInCreateMode = !carId;
  const isInEditMode = !isInCreateMode;

  useEffect(() => {
    if (isInEditMode) {
      getCarById(carId).then(car => {
        setCar(car);
        setLoadingError(null);
        setLoaded(true);
      }).catch(error => {
        setLoaded(true);
        if (error.response.status === 404) {
          setLoadingError("Car with given id not found");
        }
      });
    }

  }, [isInEditMode, carId]);

  const emptyIfNull = value => {
    return value || "";
  };

  const handleFileRead = async (event) => {
    const file = event.target.files[0];
    const base64 = await convertToBase64(file);
    updateCarField("image_base64", base64);
  };

  const handleChange = (event) => {
    updateCarField(event.target.name, event.target.value);
  };

  const updateCarField = (fieldName, value) => {
    setCar({
      ...car,
      [fieldName]: value
    });
  };

  const isSportsCar = () => {
    return car && car.type === "SPORT";
  };

  const isTruck = () => {
    return car && car.type === "TRUCK";
  };

  const handleCreateUpdateCar = () => {
    if (carId) {
      handleUpdateCar(car);
    } else {
      handleCreateCar(car);
    }
  };

  const handleUpdateCar = car => {
    updateCar(car).then(car => {
      setCar(car);
      setPostError(null);
    }).catch(error => {
      setPostError(JSON.stringify(error.response.data));
    });
  };

  const handleCreateCar = car => {
    createCar(car).then(car => {
      navigate(`/app/cars/${car.id}`, { replace: true });
    }).catch(error => {
      setPostError(JSON.stringify(error.response.data));
    });
  };

  const handleDeleteCar = () => {
    deleteCar(carId).then(() => {
      navigate("/app/cars");
    });
  };

  if (loadingError) {
    return (<Grid
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
    </Grid>);
  }


  return (
    <React.Fragment>
      {(loaded || isInCreateMode) ? (
        <Container className={classes.carDetails}>
          <Card className={clsx(classes.root)}>
            <CardContent>
              <Box display="flex" justifyContent="center" mb={3} flexDirection="column"
                   className={classes.uploadImageBox}>
                <Paper variant="outlined">
                  {car.image_base64 && (
                    <img src={emptyIfNull(car.image_base64)} alt={car.model_name} width="500px" height="250px" />)}
                </Paper>
                <input
                  accept="image/*"
                  className={classes.input}
                  style={{ display: "none" }}
                  id="raised-button-file"
                  multiple
                  type="file"
                  onChange={handleFileRead}
                />
                <label htmlFor="raised-button-file">
                  <Button variant="contained" component="span" color="primary">
                    Choose image
                  </Button>
                </label>
              </Box>
              {postError &&
              <div color="error" className={classes.errorBox}><ReactJson src={JSON.parse(postError)} theme="ocean" />
              </div>}
              <form
                autoComplete="off">
                <Grid container spacing={3}>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Model name"
                      name="model_name"
                      onChange={handleChange}
                      required
                      error={!car.model_name}
                      value={emptyIfNull(car.model_name)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>Type</InputLabel>
                      <Select
                        value={emptyIfNull(car.type)}
                        onChange={handleChange}
                        label="Type"
                        name="type"
                        required
                        error={!car.type}
                      >
                        <MenuItem value="CAR">CAR</MenuItem>
                        <MenuItem value="TRUCK">TRUCK</MenuItem>
                        <MenuItem value="SPORT">SPORT</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>Fuel type</InputLabel>
                      <Select
                        value={emptyIfNull(car.fuel_type)}
                        onChange={handleChange}
                        label="Fuel type"
                        name="fuel_type"
                        required
                        error={!car.fuel_type}
                      >
                        <MenuItem value="PETROL">PETROL</MenuItem>
                        <MenuItem value="DIESEL">DIESEL</MenuItem>
                        <MenuItem value="EV">EV</MenuItem>
                        <MenuItem value="HYBRID">HYBRID</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>Gearbox type</InputLabel>
                      <Select
                        value={emptyIfNull(car.gearbox_type)}
                        onChange={handleChange}
                        label="Gearbox type"
                        name="gearbox_type"
                        required
                        error={!car.gearbox_type}
                      >
                        <MenuItem value="AUTO">AUTO</MenuItem>
                        <MenuItem value="MANUAL">MANUAL</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>AC type</InputLabel>
                      <Select
                        value={emptyIfNull(car.ac_type)}
                        onChange={handleChange}
                        label="AC type"
                        name="ac_type"
                        required
                        error={!car.ac_type}
                      >
                        <MenuItem value="AUTO">AUTO</MenuItem>
                        <MenuItem value="MANUAL">MANUAL</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Number of passengers"
                      name="number_of_passengers"
                      type="number"
                      onChange={handleChange}
                      required
                      error={!car.number_of_passengers}
                      value={emptyIfNull(car.number_of_passengers)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>Drive type</InputLabel>
                      <Select
                        value={emptyIfNull(car.drive_type)}
                        onChange={handleChange}
                        label="Drive type"
                        name="drive_type"
                        required
                        error={!car.drive_type}
                      >
                        <MenuItem value="FRONT">FRONT</MenuItem>
                        <MenuItem value="REAR">REAR</MenuItem>
                        <MenuItem value="ALL_WHEELS">ALL WHEELS</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Average fuel consumption (l/100km)"
                      name="average_consumption"
                      type="number"
                      onChange={handleChange}
                      value={emptyIfNull(car.average_consumption)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Numbers of airbags"
                      name="number_of_airbags"
                      type="number"
                      onChange={handleChange}
                      required
                      error={!car.number_of_airbags}
                      value={emptyIfNull(car.number_of_airbags)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Boot capacity (l)"
                      name="boot_capacity"
                      type="number"
                      onChange={handleChange}
                      value={emptyIfNull(car.boot_capacity)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Price per day (PLN)"
                      name="price_per_day"
                      type="number"
                      onChange={handleChange}
                      required
                      error={!car.price_per_day}
                      value={emptyIfNull(car.price_per_day)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Deposit amount (PLN)"
                      name="deposit_amount"
                      type="number"
                      onChange={handleChange}
                      value={emptyIfNull(car.deposit_amount)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Mileage limit per day (km)"
                      name="mileage_limit"
                      type="number"
                      onChange={handleChange}
                      value={emptyIfNull(car.mileage_limit)}
                      variant="outlined"
                    />
                  </Grid>

                  {/*  TRUCK RELATED*/}
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Loading capacity (m^3)"
                      name="loading_capacity"
                      type="number"
                      onChange={handleChange}
                      value={emptyIfNull(car.loading_capacity)}
                      variant="outlined"
                      disabled={!isTruck()}
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Boot width (cm)"
                      name="boot_width"
                      type="number"
                      onChange={handleChange}
                      value={emptyIfNull(car.boot_width)}
                      variant="outlined"
                      disabled={!isTruck()}
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Boot height (cm)"
                      name="boot_height"
                      type="number"
                      onChange={handleChange}
                      value={emptyIfNull(car.boot_height)}
                      variant="outlined"
                      disabled={!isTruck()}
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Boot length (cm)"
                      name="boot_length"
                      type="number"
                      onChange={handleChange}
                      value={emptyIfNull(car.boot_length)}
                      variant="outlined"
                      disabled={!isTruck()}
                    />
                  </Grid>
                  {/*  SPORTSCAR RELATED*/}
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Horsepower"
                      name="horsepower"
                      type="number"
                      onChange={handleChange}
                      value={emptyIfNull(car.horsepower)}
                      variant="outlined"
                      disabled={!isSportsCar()}
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="0-100 time (s)"
                      name="zero_to_hundred_time"
                      type="number"
                      onChange={handleChange}
                      value={emptyIfNull(car.zero_to_hundred_time)}
                      variant="outlined"
                      disabled={!isSportsCar()}
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Engine capacity (l)"
                      name="engine_capacity"
                      type="number"
                      onChange={handleChange}
                      value={emptyIfNull(car.engine_capacity)}
                      variant="outlined"
                      disabled={!isSportsCar()}
                    />
                  </Grid>
                </Grid>
              </form>
            </CardContent>
            <CardActions disableSpacing>
              <Grid container>
                <Grid item md={6}>
                  <Button variant="contained" component="span" color="primary" onClick={handleCreateUpdateCar}>
                    Save
                  </Button>
                </Grid>
                {isInEditMode && (
                  <Grid item md={6}>
                    <Grid container justify="flex-end">
                      <Button variant="contained" component="span" color="secondary" onClick={handleDeleteCar}>
                        Delete
                      </Button>
                    </Grid>
                  </Grid>
                )}
              </Grid>
            </CardActions>
          </Card>
        </Container>
      ) : <Loading />}
    </React.Fragment>
  );
};

CreateUpdateCarForm.propTypes = {
  className: PropTypes.string,
  carId: PropTypes.string
};


export default CreateUpdateCarForm;
