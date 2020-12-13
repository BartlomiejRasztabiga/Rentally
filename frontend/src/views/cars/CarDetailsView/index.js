import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
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
import { useParams } from "react-router";
import clsx from "clsx";
import { deleteCar, getCarById, updateCar } from "../../../service/carsService";
import convertToBase64 from "../../../utils/convertToBase64";
import { useNavigate } from "react-router-dom";


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
  }
}));

const CarDetails = () => {
  const classes = useStyles();
  let { carId } = useParams();
  const navigate = useNavigate();

  const [car, setCar] = useState();

  useEffect(() => {
    getCarById(carId).then(car => {
      setCar(car);
    });
  }, [carId]);

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

  const handleUpdateCar = () => {
    updateCar(car).then(car => {
      setCar(car);
    });
  };

  const handleDeleteCar = () => {
    deleteCar(carId).then(() => {
      navigate("/app/cars")
    });
  };

  return (
    <React.Fragment>
      {car ? (
        <Container className={classes.carDetails}>
          <Card className={clsx(classes.root)}>
            <CardContent>
              <Box display="flex" justifyContent="center" mb={3}>
                <Paper variant="outlined">
                  <img src={car.image_base64} alt={car.model_name} width="500px" height="250px" />
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
                    Upload
                  </Button>
                </label>
              </Box>
              <form
                autoComplete="off"
                noValidate>
                <Grid container spacing={3}>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Model name"
                      name="model_name"
                      onChange={handleChange}
                      required
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
                      label="Average fuel consumption"
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
                      value={emptyIfNull(car.number_of_airbags)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Boot capacity"
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
                      label="Price per day"
                      name="price_per_day"
                      type="number"
                      onChange={handleChange}
                      required
                      value={emptyIfNull(car.price_per_day)}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={6} xs={12}>
                    <TextField
                      fullWidth
                      label="Deposit amount"
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
                      label="Mileage limit"
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
                      label="Loading capacity"
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
                      label="Boot width"
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
                      label="Boot height"
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
                      label="Boot length"
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
                      label="0-100 time"
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
                      label="Engine capacity"
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
                  <Button variant="contained" component="span" color="primary" onClick={handleUpdateCar}>
                    Update
                  </Button>
                </Grid>
                <Grid item md={6}>
                  <Button variant="contained" component="span" color="secondary" onClick={handleDeleteCar}>
                    Delete
                  </Button>
                </Grid>
              </Grid>
            </CardActions>
          </Card>
        </Container>
      ) : (<Grid
        container
        spacing={0}
        direction="column"
        alignItems="center"
        justify="center"
        style={{ minHeight: "100vh" }}
      >
        <Grid item xs={3}>
          <Typography variant="h2">Loading...</Typography>
        </Grid>
      </Grid>)}
    </React.Fragment>
  );
};

CarDetails.propTypes = {
  className: PropTypes.string,
  carId: PropTypes.number
};

export default CarDetails;
