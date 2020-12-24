import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  FormControl,
  Grid,
  InputLabel,
  makeStyles,
  MenuItem,
  Select,
  TextField,
} from "@material-ui/core";
import Page from "../../../components/Page";
import CarCard from "../../../components/cars/CarCard";
import { getCars, getCarsWithSearchQuery } from "../../../service/carsService";
import { useNavigate } from "react-router";
import { APP_CARS_URL } from "../../../config";
import Slider from "@material-ui/core/Slider";
import Typography from "@material-ui/core/Typography";
import { DateTimePicker } from "@material-ui/pickers";

const searchQueryInitialState = {
  model_name: "",
  type: "",
  fuel_type: "",
  gearbox_type: "",
  ac_type: "",
  drive_type: "",
  number_of_passengers: [0, 100],
  price_per_day: [1.0, 500.0],
  start_date: null,
  end_date: null,
};

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: "100%",
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3),
  },
  carCard: {
    height: "100%",
  },
}));

const CarsList = () => {
  const classes = useStyles();
  const navigate = useNavigate();
  const [cars, setCars] = useState([]);
  const [searchQuery, setSearchQuery] = useState(searchQueryInitialState);

  useEffect(() => {
    getCars().then((_cars) => {
      setCars(_cars);
    });
  }, []);

  const handleAddCar = () => {
    navigate(`${APP_CARS_URL}/new`);
  };

  const handleChangeSearchQuery = (event) => {
    updateSearchQueryField(event.target.name, event.target.value);
  };

  const handleNumberOfPassengersRangeChange = (event, newValue) => {
    updateSearchQueryField("number_of_passengers", newValue);
  };

  const handlePricePerDayRangeChange = (event, newValue) => {
    updateSearchQueryField("price_per_day", newValue);
  };

  const handleStartDateChange = (date) => {
    updateSearchQueryField("start_date", date.format());
  };

  const handleEndDateChange = (date) => {
    updateSearchQueryField("end_date", date.format());
  };

  const updateSearchQueryField = (fieldName, value) => {
    setSearchQuery({
      ...searchQuery,
      [fieldName]: value,
    });
  };

  const handleResetFilter = () => {
    setSearchQuery(searchQueryInitialState);
    getCars().then((_cars) => {
      setCars(_cars);
    });
  };

  const handleFilter = () => {
    getCarsWithSearchQuery(searchQuery).then((_cars) => {
      setCars(_cars);
    });
  };

  return (
    <Page className={classes.root}>
      <Container maxWidth={false}>
        <Box display="flex" justifyContent="flex-end">
          <Button color="primary" variant="contained" onClick={handleAddCar}>
            Add car
          </Button>
        </Box>
        <Box mt={3}>
          <Card>
            <CardContent>
              <form autoComplete="off">
                <Grid container spacing={3}>
                  <Grid item md={3} xs={6}>
                    <TextField
                      fullWidth
                      label="Model name"
                      name="model_name"
                      onChange={handleChangeSearchQuery}
                      value={searchQuery.model_name}
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={3} xs={6}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>Type</InputLabel>
                      <Select
                        value={searchQuery.type}
                        onChange={handleChangeSearchQuery}
                        label="Type"
                        name="type"
                      >
                        <MenuItem value="">EMPTY</MenuItem>
                        <MenuItem value="CAR">CAR</MenuItem>
                        <MenuItem value="TRUCK">TRUCK</MenuItem>
                        <MenuItem value="SPORT">SPORT</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={3} xs={6}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>Fuel type</InputLabel>
                      <Select
                        value={searchQuery.fuel_type}
                        onChange={handleChangeSearchQuery}
                        label="Fuel type"
                        name="fuel_type"
                      >
                        <MenuItem value="">EMPTY</MenuItem>
                        <MenuItem value="PETROL">PETROL</MenuItem>
                        <MenuItem value="DIESEL">DIESEL</MenuItem>
                        <MenuItem value="HYBRID">HYBRID</MenuItem>
                        <MenuItem value="EV">EV</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={3} xs={6}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>Gearbox type</InputLabel>
                      <Select
                        value={searchQuery.gearbox_type}
                        onChange={handleChangeSearchQuery}
                        label="Gearbox type"
                        name="gearbox_type"
                      >
                        <MenuItem value="">EMPTY</MenuItem>
                        <MenuItem value="AUTO">AUTO</MenuItem>
                        <MenuItem value="MANUAL">MANUAL</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={3} xs={6}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>AC type</InputLabel>
                      <Select
                        value={searchQuery.ac_type}
                        onChange={handleChangeSearchQuery}
                        label="AC type"
                        name="ac_type"
                      >
                        <MenuItem value="">EMPTY</MenuItem>
                        <MenuItem value="AUTO">AUTO</MenuItem>
                        <MenuItem value="MANUAL">MANUAL</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={3} xs={6}>
                    <FormControl variant="outlined" fullWidth>
                      <InputLabel>Drive type</InputLabel>
                      <Select
                        value={searchQuery.drive_type}
                        onChange={handleChangeSearchQuery}
                        label="Drive type"
                        name="drive_type"
                      >
                        <MenuItem value="">EMPTY</MenuItem>
                        <MenuItem value="FRONT">FRONT</MenuItem>
                        <MenuItem value="REAR">REAR</MenuItem>
                        <MenuItem value="ALL_WHEELS">ALL WHEELS</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item md={3} xs={6}>
                    <Typography id="range-slider" gutterBottom>
                      Number of passengers
                    </Typography>
                    <Slider
                      value={searchQuery.number_of_passengers}
                      onChange={handleNumberOfPassengersRangeChange}
                      valueLabelDisplay="auto"
                      aria-labelledby="range-slider"
                      label="Number of passengers"
                      name="number_of_passengers"
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={3} xs={6}>
                    <Typography id="range-slider" gutterBottom>
                      Price per day
                    </Typography>
                    <Slider
                      value={searchQuery.price_per_day}
                      onChange={handlePricePerDayRangeChange}
                      valueLabelDisplay="auto"
                      aria-labelledby="range-slider"
                      min={1.0}
                      max={500.0}
                      step={10.0}
                      label="Price per day"
                      name="price_per_day"
                      variant="outlined"
                    />
                  </Grid>
                  <Grid item md={3} xs={6}>
                    <DateTimePicker
                      fullWidth
                      showTodayButton
                      ampm={false}
                      label="Start date"
                      name="start_date"
                      inputVariant="outlined"
                      disablePast
                      onChange={handleStartDateChange}
                      value={searchQuery.start_date}
                    />
                  </Grid>
                  <Grid item md={3} xs={6}>
                    <DateTimePicker
                      fullWidth
                      showTodayButton
                      ampm={false}
                      label="End date"
                      name="end_date"
                      inputVariant="outlined"
                      disablePast
                      onChange={handleEndDateChange}
                      value={searchQuery.end_date}
                    />
                  </Grid>
                  <Grid item md={3} xs={6}>
                    <Button variant="contained" onClick={handleResetFilter}>
                      Reset filter
                    </Button>
                  </Grid>
                  <Grid item md={3} xs={6}>
                    <Button
                      variant="contained"
                      // component="span"
                      color="primary"
                      onClick={handleFilter}
                    >
                      Filter
                    </Button>
                  </Grid>
                </Grid>
              </form>
            </CardContent>
          </Card>
        </Box>
        <Box mt={3}>
          <Grid container spacing={3}>
            {cars.map((car) => (
              <Grid item key={car.id} lg={4} md={4} xs={12}>
                <CarCard className={classes.carCard} car={car} />
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
    </Page>
  );
};

export default CarsList;
