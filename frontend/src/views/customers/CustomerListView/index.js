import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  InputAdornment,
  makeStyles,
  SvgIcon,
  TextField
} from "@material-ui/core";
import Page from "src/components/Page";
import CustomersList from "./CustomersList";
import SearchIcon from "@material-ui/icons/Search";
import { getCustomers } from "../../../service/customersService";
import { useNavigate } from "react-router";

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: "100%",
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  }
}));

const CustomersListView = () => {
  const classes = useStyles();
  const navigate = useNavigate();
  const [customers, setCustomers] = useState([]);
  const [searchPhrase, setSearchPhrase] = useState("");

  useEffect(() => {
    getCustomers().then(customers => {
      setCustomers(customers);
    });
  }, []);

  const handleAddCustomer = () => {
    navigate("/app/customers/new");
  };

  const filterCustomersBasedOnSearchPhrase = () => {
    return customers.filter(customer => customer.full_name.toLowerCase().includes(searchPhrase.toLowerCase()));
  };

  return (
    <Page className={classes.root}>
      <Container maxWidth={false}>
        {/*TODO can extract this search box to another component and share state? redux or react context?*/}
        {/*Should share it with CarsListView*/}
        <Box display="flex" justifyContent="flex-end">
          <Button color="primary" variant="contained" onClick={handleAddCustomer}>
            Add customer
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
                  placeholder="Search customer"
                  variant="outlined"
                />
              </Box>
            </CardContent>
          </Card>
        </Box>
        <Box mt={3}>
          <CustomersList
            customers={filterCustomersBasedOnSearchPhrase()} />
        </Box>
      </Container>
    </Page>
  );
};

export default CustomersListView;
