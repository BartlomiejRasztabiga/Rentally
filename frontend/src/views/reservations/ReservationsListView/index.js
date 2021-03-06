import React, { useEffect, useState } from "react";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import { useNavigate } from "react-router";
import { getReservations } from "../../../service/reservationsService";
import ReservationsList from "../../../components/reservations/ReservationsList";
import { APP_RESERVATIONS_URL } from "../../../config";

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: "100%",
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3),
  },
}));

const ReservationsListView = () => {
  const classes = useStyles();
  const navigate = useNavigate();
  const [reservations, setReservations] = useState([]);

  useEffect(() => {
    getReservations().then((_reservations) => {
      setReservations(_reservations);
    });
  }, []);

  const handleAddReservation = () => {
    navigate(`${APP_RESERVATIONS_URL}/new`);
  };

  return (
    <Container maxWidth={false} className={classes.root}>
      <Box display="flex" justifyContent="flex-end">
        <Button
          color="primary"
          variant="contained"
          onClick={handleAddReservation}
        >
          Add reservation
        </Button>
      </Box>
      <Box mt={3}>
        <ReservationsList reservations={reservations} />
      </Box>
    </Container>
  );
};

export default ReservationsListView;
