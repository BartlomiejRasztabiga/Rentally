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
import RentalRow from "./RentalRow";

const useStyles = makeStyles((theme) => ({
  root: {},
}));

const RentalsList = ({ className, rentals, ...rest }) => {
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
              <TableCell>Reservation</TableCell>
              <TableCell>Start date</TableCell>
              <TableCell>End date</TableCell>
              <TableCell>Status</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {rentals.map((rental, key) => (
              <RentalRow rental={rental} key={key} />
            ))}
          </TableBody>
        </Table>
      </Box>
    </Card>
  );
};

RentalsList.propTypes = {
  className: PropTypes.string,
  rentals: PropTypes.array.isRequired,
};

export default RentalsList;
