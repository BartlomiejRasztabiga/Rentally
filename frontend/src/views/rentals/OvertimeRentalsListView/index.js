import React, { useEffect, useState } from "react";
import { Box, Container, makeStyles } from "@material-ui/core";
import { getOvertimeRentals } from "../../../service/rentalsService";
import RentalsList from "../../../components/rentals/RentalsList";
import Page from "../../../components/Page";

const useStyles = makeStyles((theme) => ({
  root: {
    paddingTop: theme.spacing(3),
  },
}));

const OvertimeRentalsListView = () => {
  const classes = useStyles();
  const [rentals, setRentals] = useState([]);

  useEffect(() => {
    getOvertimeRentals().then((_rentals) => {
      setRentals(_rentals);
    });
  }, []);

  return (
    <Page className={classes.root}>
      <Container maxWidth={false}>
        <Box dmt={3}>
          <RentalsList rentals={rentals} />
        </Box>
      </Container>
    </Page>
  );
};

export default OvertimeRentalsListView;
