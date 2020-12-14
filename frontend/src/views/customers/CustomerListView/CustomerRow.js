import React from "react";
import PropTypes from "prop-types";
import { Avatar, Box, Button, makeStyles, TableCell, TableRow, Typography } from "@material-ui/core";
import getInitials from "../../../utils/getInitials";
import { Link } from "react-router-dom";
import clsx from "clsx";

const useStyles = makeStyles((theme) => ({
  root: {},
  link: {
    color: "inherit",
    textDecoration: "none"
  },
  customerName: {
    marginLeft: theme.spacing(1)
  }
}));

const Customer = ({ className, customer, ...rest }) => {
  const classes = useStyles();

  return (
    <TableRow hover key={customer.id} className={clsx(classes.root, className)} {...rest}>
      <TableCell>
        <Box alignItems="center" display="flex">
          <Avatar className={classes.avatar}>
            {getInitials(customer.full_name)}
          </Avatar>
          <Typography className={classes.customerName} color="textPrimary" variant="body1">
            {customer.full_name}
          </Typography>
        </Box>
      </TableCell>
      <TableCell>
        {customer.address}
      </TableCell>
      <TableCell>{customer.phone_number}</TableCell>
      <TableCell>
        <Button color="primary" variant="contained">
          <Link className={classes.link} to={`/app/customers/${customer.id}`}>DETAILS</Link>
        </Button>
      </TableCell>
    </TableRow>
  );
};

Customer.propTypes = {
  className: PropTypes.string,
  customer: PropTypes.object.isRequired
};

export default Customer;