import React, { useEffect, useState } from "react";
import { Box, Button, Container, makeStyles } from "@material-ui/core";
import { useNavigate } from "react-router";
import { APP_RENTALS_URL } from "../../../config";
import { getRentals } from "../../../service/rentalsService";
import RentalsList from "../../../components/rentals/RentalsList";

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: "100%",
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3),
  },
}));

const RentalsListView = () => {
  const classes = useStyles();
  const navigate = useNavigate();
  const [rentals, setRentals] = useState([]);

  useEffect(() => {
    getRentals().then((_rentals) => {
      setRentals(_rentals);
    });
  }, []);

  const handleAddRental = () => {
    navigate(`${APP_RENTALS_URL}/new`);
  };

  return (
    <Container maxWidth={false} className={classes.root}>
      <Box display="flex" justifyContent="flex-end">
        <Button color="primary" variant="contained" onClick={handleAddRental}>
          Add rental
        </Button>
      </Box>
      <Box mt={3}>
        <RentalsList rentals={rentals} />
      </Box>
    </Container>
  );
};

export default RentalsListView;
