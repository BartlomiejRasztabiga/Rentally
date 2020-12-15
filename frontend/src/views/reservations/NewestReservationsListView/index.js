import React, { useEffect, useState } from "react";
import clsx from "clsx";
import PerfectScrollbar from "react-perfect-scrollbar";
import PropTypes from "prop-types";
import { Box, Button, Card, CardHeader, Divider, makeStyles } from "@material-ui/core";
import ArrowRightIcon from "@material-ui/icons/ArrowRight";
import { getReservations } from "../../../service/reservationsService";
import ReservationsList from "../ReservationsListView/ReservationsList";
import { Link } from "react-router-dom";


const useStyles = makeStyles(() => ({
  root: {},
  actions: {
    justifyContent: "flex-end"
  },
  link: {
    color: "inherit",
    textDecoration: "none"
  }
}));

const sortReservationsByDate = (reservations) => {
  return reservations.sort((a, b) => {
    return new Date(b.start_date) - new Date(a.start_date);
  });
};

const NewestReservations = ({ className, ...rest }) => {
  const classes = useStyles();
  const [reservations, setReservations] = useState([]);

  useEffect(() => {
    getReservations().then(reservations => {
      setReservations(reservations);
    });
  }, []);

  return (
    <Card className={clsx(classes.root, className)} {...rest}>
      <CardHeader title="Newest Reservations" />
      <Divider />
      <PerfectScrollbar>
        <ReservationsList reservations={sortReservationsByDate(reservations).slice(0, 5)} />
      </PerfectScrollbar>
      <Box display="flex" justifyContent="flex-end" p={2}>
        <Button
          color="primary"
          endIcon={<ArrowRightIcon />}
          size="small"
          variant="text"
        >
          <Link className={classes.link} to={"/app/reservations"}>View all</Link>

        </Button>
      </Box>
    </Card>
  );
};

NewestReservations.propTypes = {
  className: PropTypes.string
};

export default NewestReservations;