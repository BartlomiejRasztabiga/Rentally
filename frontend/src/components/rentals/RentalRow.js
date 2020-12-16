import React from "react";
import PropTypes from "prop-types";
import {
  Box,
  Button,
  makeStyles,
  TableCell,
  TableRow,
  Typography,
} from "@material-ui/core";
import { Link } from "react-router-dom";
import clsx from "clsx";
import moment from "moment";
import {
  APP_CARS_URL,
  APP_CUSTOMERS_URL,
  APP_RENTALS_URL,
  APP_RESERVATIONS_URL,
} from "../../config";

const useStyles = makeStyles((theme) => ({
  root: {},
  link: {
    color: "inherit",
    textDecoration: "none",
  },
  relatedObjectLink: {
    color: theme.palette.primary.main,
    fontSize: "larger",
  },
}));

const RentalRow = ({ className, rental, ...rest }) => {
  const classes = useStyles();

  const formatDate = (date) => {
    return moment(date).format("DD.M.YYYY HH:mm");
  };

  return (
    <TableRow
      hover
      key={rental.id}
      className={clsx(classes.root, className)}
      {...rest}
    >
      <TableCell>
        <Box alignItems="center" display="flex">
          <Typography
            className={classes.customerName}
            color="textPrimary"
            variant="body1"
          >
            {rental.id}
          </Typography>
        </Box>
      </TableCell>
      <TableCell>
        <Link
          className={classes.relatedObjectLink}
          to={`${APP_CARS_URL}/${rental.car_id}`}
        >
          {rental.car.model_name}
        </Link>
      </TableCell>
      <TableCell>
        <Link
          className={classes.relatedObjectLink}
          to={`${APP_CUSTOMERS_URL}/${rental.customer_id}`}
        >
          {rental.customer.full_name}
        </Link>
      </TableCell>
      <TableCell>
        {rental.reservation_id && (
          <Link
            className={classes.relatedObjectLink}
            to={`${APP_RESERVATIONS_URL}/${rental.reservation_id}`}
          >
            {rental.reservation_id}
          </Link>
        )}
      </TableCell>
      <TableCell>{formatDate(rental.start_date)}</TableCell>
      <TableCell>{formatDate(rental.end_date)}</TableCell>
      <TableCell>{rental.status}</TableCell>
      <TableCell>
        <Button color="primary" variant="contained">
          <Link className={classes.link} to={`${APP_RENTALS_URL}/${rental.id}`}>
            DETAILS
          </Link>
        </Button>
      </TableCell>
    </TableRow>
  );
};

RentalRow.propTypes = {
  className: PropTypes.string,
  rental: PropTypes.object.isRequired,
};

export default RentalRow;
