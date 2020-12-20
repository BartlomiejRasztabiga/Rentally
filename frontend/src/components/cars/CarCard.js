import React from "react";
import PropTypes from "prop-types";
import clsx from "clsx";
import {
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  Grid,
  makeStyles,
  Paper,
  Typography,
} from "@material-ui/core";
import LocalGasStationIcon from "@material-ui/icons/LocalGasStation";
import SettingsIcon from "@material-ui/icons/Settings";
import PersonIcon from "@material-ui/icons/Person";
import AttachMoneyIcon from "@material-ui/icons/AttachMoney";
import AcUnitIcon from "@material-ui/icons/AcUnit";
import { Link } from "react-router-dom";
import { APP_CARS_URL } from "../../config";

const EMPTY_IMG_BASE64 =
  "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column",
  },
  statsItem: {
    alignItems: "center",
    display: "flex",
  },
  statsIcon: {
    marginRight: theme.spacing(1),
  },
  large: {
    width: theme.spacing(20),
    height: theme.spacing(20),
  },
  link: {
    color: "inherit",
    textDecoration: "none",
  },
  carImage: {
    objectFit: "cover"
  }
}));

const CarCard = ({ className, car, ...rest }) => {
  const classes = useStyles();

  return (
    <Card className={clsx(classes.root, className)} {...rest}>
      <CardContent>
        <Box display="flex" justifyContent="center" mb={3}>
          <Paper variant="outlined">
            <img
              src={car.image_base64 || EMPTY_IMG_BASE64}
              alt={car.model_name}
              width="500px"
              height="250px"
              className={classes.carImage}
            />
          </Paper>
        </Box>
        <Grid container justify="space-between">
          <Typography
            align="left"
            color="textPrimary"
            gutterBottom
            variant="h4"
          >
            {car.model_name}
          </Typography>
          <Button variant="contained" color="primary">
            <Link className={classes.link} to={`${APP_CARS_URL}/${car.id}`}>
              DETAILS
            </Link>
          </Button>
        </Grid>
      </CardContent>
      <Box flexGrow={1} />
      <Divider />
      <Box p={2}>
        <Grid container justify="space-between" spacing={2}>
          <Grid className={classes.statsItem} item lg={3} md={3}>
            <LocalGasStationIcon />
            <Typography color="textPrimary" variant="h6">
              {car.fuel_type}
            </Typography>
          </Grid>
          <Grid className={classes.statsItem} item lg={3} md={3}>
            <SettingsIcon />
            <Typography color="textPrimary" variant="h6">
              {car.gearbox_type}
            </Typography>
          </Grid>
          <Grid className={classes.statsItem} item lg={4} md={4}>
            <AttachMoneyIcon />
            <Typography color="textPrimary" variant="h5">
              {car.price_per_day} PLN / day
            </Typography>
          </Grid>
        </Grid>
        <Grid container justify="space-between" spacing={2}>
          <Grid className={classes.statsItem} item lg={3} md={3}>
            <AcUnitIcon />
            <Typography color="textPrimary" variant="h6">
              {car.ac_type}
            </Typography>
          </Grid>
          <Grid className={classes.statsItem} item lg={3} md={3}>
            <PersonIcon />
            <Typography color="textPrimary" variant="h6">
              {car.number_of_passengers}
            </Typography>
          </Grid>
          <Grid className={classes.statsItem} item lg={4} md={4}>
            <AttachMoneyIcon />
            <Typography color="textPrimary" variant="h6">
              {car.deposit_amount
                ? `${car.deposit_amount} PLN deposit`
                : "no deposit"}
            </Typography>
          </Grid>
        </Grid>
      </Box>
    </Card>
  );
};

CarCard.propTypes = {
  className: PropTypes.string,
  car: PropTypes.object.isRequired,
};

export default CarCard;
