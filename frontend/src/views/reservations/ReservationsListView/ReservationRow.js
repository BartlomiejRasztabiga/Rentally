import React from "react";
import PropTypes from "prop-types";
import { Box, Button, makeStyles, TableCell, TableRow, Typography } from "@material-ui/core";
import { Link } from "react-router-dom";
import clsx from "clsx";
import moment from "moment";

const useStyles = makeStyles((theme) => ({
  root: {},
  link: {
    color: "inherit",
    textDecoration: "none"
  },
  relatedObjectLink: {
    color: theme.palette.primary.main,
    fontSize: "larger"
  }
}));

const Reservation = ({ className, reservation, ...rest }) => {
  const classes = useStyles();

  const formatDate = date => {
    return moment(date).format("DD.M.YYYY hh:mm");
  };

  return (
    <TableRow hover key={reservation.id} className={clsx(classes.root, className)} {...rest}>
      <TableCell>
        <Box alignItems="center" display="flex">
          <Typography className={classes.customerName} color="textPrimary" variant="body1">
            {reservation.id}
          </Typography>
        </Box>
      </TableCell>
      <TableCell>
        <Link className={classes.relatedObjectLink}
              to={`/app/cars/${reservation.car_id}`}>{reservation.car.model_name}</Link>
      </TableCell>
      <TableCell>
        <Link className={classes.relatedObjectLink}
              to={`/app/customers/${reservation.customer_id}`}>{reservation.customer.full_name}</Link>
      </TableCell>
      <TableCell>{formatDate(reservation.start_date)}</TableCell>
      <TableCell>{formatDate(reservation.end_date)}</TableCell>
      <TableCell>{reservation.status}</TableCell>
      <TableCell>
        <Button color="primary" variant="contained">
          <Link className={classes.link} to={`/app/reservations/${reservation.id}`}>DETAILS</Link>
        </Button>
      </TableCell>
    </TableRow>
  );
};

Reservation.propTypes = {
  className: PropTypes.string,
  reservation: PropTypes.object.isRequired
};

export default Reservation;
