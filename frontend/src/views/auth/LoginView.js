import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Container,
  makeStyles,
  TextField,
  Typography,
} from "@material-ui/core";
import { useAuth } from "../../context/auth";
import { getAccessToken } from "../../service/authService";
import { APP_DASHBOARD_URL } from "../../config";

const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    height: "100%",
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3),
  },

  errorMessage: {
    color: "red",
  },
}));

const LoginView = () => {
  const classes = useStyles();
  const navigate = useNavigate();
  const { setAccessToken } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [isLoggedIn, setLoggedIn] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = () => {
    setIsSubmitting(true);

    getAccessToken(email, password)
      .then((response) => {
        setIsSubmitting(false);
        setError(null);

        setAccessToken(response.data.access_token);
        setLoggedIn(true);
      })
      .catch((_error) => {
        if (_error.response) {
          const errorMsg = _error.response.data.detail;
          setError(errorMsg);
        }
        setIsSubmitting(false);
      });
  };

  useEffect(() => {
    if (isLoggedIn) navigate(APP_DASHBOARD_URL, { replace: true });
  }, [navigate, isLoggedIn]);

  return (
    <Box
      display="flex"
      flexDirection="column"
      height="100%"
      justifyContent="center"
      className={classes.root}
    >
      <Container maxWidth="sm">
        <form>
          <Box mb={3}>
            <Typography color="textPrimary" variant="h2">
              Sign in
            </Typography>
          </Box>
          <TextField
            fullWidth
            label="Email Address"
            margin="normal"
            name="email"
            onChange={handleEmailChange}
            type="email"
            value={email}
            variant="outlined"
          />
          <TextField
            fullWidth
            label="Password"
            margin="normal"
            name="password"
            onChange={handlePasswordChange}
            type="password"
            value={password}
            variant="outlined"
          />
          {error ? <div className={classes.errorMessage}>{error}</div> : null}
          <Box my={2}>
            <Button
              color="primary"
              disabled={isSubmitting}
              fullWidth
              size="large"
              type="submit"
              variant="contained"
              onClick={handleSubmit}
            >
              Sign in
            </Button>
          </Box>
        </form>
      </Container>
    </Box>
  );
};

export default LoginView;
