import React from "react";
import PropTypes from "prop-types";
import clsx from "clsx";
import { Box, Card, CardContent, Divider, Grid, makeStyles, Paper, Typography } from "@material-ui/core";
import LocalGasStationIcon from "@material-ui/icons/LocalGasStation";
import SettingsIcon from "@material-ui/icons/Settings";
import PersonIcon from "@material-ui/icons/Person";
import AttachMoneyIcon from "@material-ui/icons/AttachMoney";
import AcUnitIcon from "@material-ui/icons/AcUnit";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexDirection: "column"
  },
  statsItem: {
    alignItems: "center",
    display: "flex"
  },
  statsIcon: {
    marginRight: theme.spacing(1)
  },
  large: {
    width: theme.spacing(20),
    height: theme.spacing(20)
  }
}));

const CarCard = ({ className, car, ...rest }) => {
  const classes = useStyles();

  return (
    <Card className={clsx(classes.root, className)} {...rest}>
      <CardContent>
        <Box display="flex" justifyContent="center" mb={3}>
          <Paper variant="outlined">
            <img src={car.media} alt={car.modelName} width="500px" height="250px" />
          </Paper>
        </Box>
        <Typography align="left" color="textPrimary" gutterBottom variant="h4">
          {car.modelName}
        </Typography>
        <Typography align="center" color="textPrimary" variant="body1">
          {car.description}
        </Typography>
      </CardContent>
      <Box flexGrow={1} />
      <Divider />
      <Box p={2}>
        <Grid container justify="space-between" spacing={2}>
          <Grid className={classes.statsItem} item lg={3} md={3}>
            <LocalGasStationIcon />
            <Typography color="textPrimary" variant="h7">{car.fuelType}</Typography>
          </Grid>
          <Grid className={classes.statsItem} item lg={3} md={3}>
            <SettingsIcon />
            <Typography color="textPrimary" variant="h7">{car.gearboxType}</Typography>
          </Grid>
          <Grid className={classes.statsItem} item lg={4} md={4}>
            <AttachMoneyIcon />
            <Typography color="textPrimary" variant="h5">{car.pricePerDay} zł / dzień</Typography>
          </Grid>
        </Grid>
        <Grid container justify="space-between" spacing={2}>
          <Grid className={classes.statsItem} item lg={3} md={3}>
            <AcUnitIcon />
            <Typography color="textPrimary" variant="h7">{car.acType}</Typography>
          </Grid>
          <Grid className={classes.statsItem} item lg={3} md={3}>
            <PersonIcon />
            <Typography color="textPrimary" variant="h7">{car.numberOfPassengers}</Typography>
          </Grid>
          <Grid className={classes.statsItem} item lg={4} md={4}>
            <AttachMoneyIcon />
            <Typography color="textPrimary" variant="h6">{car.depositAmount} zł kaucji</Typography>
          </Grid>
        </Grid>
      </Box>
    </Card>
  );
};

CarCard.propTypes = {
  className: PropTypes.string,
  car: PropTypes.object.isRequired
};

export default CarCard;
