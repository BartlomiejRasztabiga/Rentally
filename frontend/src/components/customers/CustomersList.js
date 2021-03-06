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
import CustomerRow from "./CustomerRow";

const useStyles = makeStyles((theme) => ({
  root: {},
}));

const CustomersList = ({ className, customers, ...rest }) => {
  const classes = useStyles();

  return (
    <Card className={clsx(classes.root, className)} {...rest}>
      <Box minWidth={1050}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Address</TableCell>
              <TableCell>Phone number</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {customers.map((customer, key) => (
              <CustomerRow customer={customer} key={key} />
            ))}
          </TableBody>
        </Table>
      </Box>
    </Card>
  );
};

CustomersList.propTypes = {
  className: PropTypes.string,
  customers: PropTypes.array.isRequired,
};

export default CustomersList;
