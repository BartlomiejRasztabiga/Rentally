import React, { useEffect, useState } from "react";
import clsx from "clsx";
import PerfectScrollbar from "react-perfect-scrollbar";
import PropTypes from "prop-types";
import {
  Box,
  Button,
  Card,
  CardHeader,
  Divider,
  makeStyles,
} from "@material-ui/core";
import ArrowRightIcon from "@material-ui/icons/ArrowRight";
import { Link } from "react-router-dom";
import { APP_RENTALS_URL } from "../../../config";
import { getRentals } from "../../../service/rentalsService";
import RentalsList from "../../../components/rentals/RentalsList";

const useStyles = makeStyles(() => ({
  root: {},
  actions: {
    justifyContent: "flex-end",
  },
  link: {
    color: "inherit",
    textDecoration: "none",
  },
}));

const sortRentalsByDate = (rentals) => {
  return rentals.sort((a, b) => {
    return new Date(a.start_date) - new Date(b.start_date);
  });
};

const NewestRentalsListView = ({ className, ...rest }) => {
  const classes = useStyles();
  const [rentals, setRentals] = useState([]);

  useEffect(() => {
    getRentals().then((_rentals) => {
      setRentals(_rentals);
    });
  }, []);

  return (
    <Card className={clsx(classes.root, className)} {...rest}>
      <CardHeader title="Newest Rentals" />
      <Divider />
      <PerfectScrollbar>
        <RentalsList rentals={sortRentalsByDate(rentals).slice(0, 5)} />
      </PerfectScrollbar>
      <Box display="flex" justifyContent="flex-end" p={2}>
        <Button
          color="primary"
          endIcon={<ArrowRightIcon />}
          size="small"
          variant="text"
        >
          <Link className={classes.link} to={APP_RENTALS_URL}>
            View all
          </Link>
        </Button>
      </Box>
    </Card>
  );
};

NewestRentalsListView.propTypes = {
  className: PropTypes.string,
};

export default NewestRentalsListView;
