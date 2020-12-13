import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Grid,
  InputAdornment,
  makeStyles,
  SvgIcon,
  TextField
} from "@material-ui/core";
import Page from "src/components/Page";
import CarCard from "./CarCard";
import { getCars } from "../../../service/carsService";
import { Search as SearchIcon } from "react-feather";

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
  const [cars, setCars] = useState([]);
  const [searchPhrase, setSearchPhrase] = useState("");

  useEffect(() => {
    getCars().then(cars => {
      setCars(cars);
    });
  }, []);

  return (
    <Page className={classes.root}>
      <Container maxWidth={false}>
        {/*TODO can extract this earch box to another component and share state? redux or react context?*/}
        <Box display="flex" justifyContent="flex-end">
          <Button color="primary" variant="contained">
            Add car
          </Button>
        </Box>
        <Box mt={3}>
          <Card>
            <CardContent>
              <Box maxWidth={500}>
                <TextField
                  fullWidth
                  value={searchPhrase}
                  onChange={e => setSearchPhrase(e.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SvgIcon fontSize="small" color="action">
                          <SearchIcon />
                        </SvgIcon>
                      </InputAdornment>
                    )
                  }}
                  placeholder="Search car"
                  variant="outlined"
                />
              </Box>
            </CardContent>
          </Card>
        </Box>
        <Box mt={3}>
          <Grid container spacing={3}>
            {cars.filter(car => car.model_name.toLowerCase().includes(searchPhrase.toLowerCase())).map((car) => (
              <Grid item key={car.id} lg={4} md={4} xs={12}>
                <CarCard className={classes.carCard} car={car} />
              </Grid>
            ))}
          </Grid>
        </Box>
      </Container>
    </Page>
  );
};

export default CarsList;
