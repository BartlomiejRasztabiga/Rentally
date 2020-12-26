import React from "react";
import clsx from "clsx";
import PropTypes from "prop-types";
import {
  Box,
  Card,
  makeStyles,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@material-ui/core";
import ReservationRow from "./ReservationRow";

const useStyles = makeStyles((theme) => ({
  root: {},
}));

const ReservationsList = ({ className, reservations, ...rest }) => {
  const classes = useStyles();

  return (
    <Card className={clsx(classes.root, className)} {...rest}>
      <Box minWidth={1050}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Car</TableCell>
              <TableCell>Customer</TableCell>
              <TableCell>Start date</TableCell>
              <TableCell>End date</TableCell>
              <TableCell>Status</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {reservations.map((reservation, key) => (
              <ReservationRow reservation={reservation} key={key} />
            ))}
          </TableBody>
        </Table>
      </Box>
    </Card>
  );
};

ReservationsList.propTypes = {
  className: PropTypes.string,
  reservations: PropTypes.array.isRequired,
};

export default ReservationsList;
