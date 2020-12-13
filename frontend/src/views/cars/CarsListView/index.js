import React, { useState } from "react";
import { Box, Container, Grid, makeStyles } from "@material-ui/core";
import Page from "src/components/Page";
import Toolbar from "./Toolbar";
import CarCard from "./CarCard";

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: "100%",
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  },
  carCard: {
    height: "100%"
  }
}));

const CarsList = () => {
  const classes = useStyles();
  // const [cars] = useState(data);

  return (
    <Page className={classes.root}>
      <Container maxWidth={false}>
        <Toolbar />
        <Box mt={3}>
          <Grid container spacing={3}>
            {/*{cars.map((car) => (*/}
            {/*  <Grid item key={car.id} lg={4} md={4} xs={12}>*/}
            {/*    <CarCard className={classes.carCard} car={car} />*/}
            {/*  </Grid>*/}
            {/*))}*/}
          </Grid>
        </Box>
      </Container>
    </Page>
  );
};

export default CarsList;
