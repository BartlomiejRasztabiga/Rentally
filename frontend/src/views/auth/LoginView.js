import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import * as Yup from "yup";
import axios from "../../service/axios";
import { Formik } from "formik";
import {
  Box,
  Button,
  Container,
  makeStyles,
  TextField,
  Typography,
} from "@material-ui/core";
import Page from "../../components/Page";
import { ACCESS_TOKEN_URL } from "../../config";
import { useAuth } from "../../context/auth";

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
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [error, setError] = useState(null);
  const { setAccessToken } = useAuth();

  const postLogin = (values, actions) => {
    const username = values.email;
    const password = values.password;

    const bodyFormData = new FormData();
    bodyFormData.append("username", username);
    bodyFormData.append("password", password);

    axios({
      method: "post",
      url: `${ACCESS_TOKEN_URL}/`,
      data: bodyFormData,
      headers: { "Content-Type": "multipart/form-data" },
    })
      .then(function (response) {
        actions.setSubmitting(false);
        actions.resetForm();

        setError(null);

        setAccessToken(response.data.access_token);
        setLoggedIn(true);
      })
      .catch(function (_error) {
        if (_error.response) {
          const errorMsg = _error.response.data.detail;
          setError(errorMsg);
        }
        actions.setSubmitting(false);
      });
  };

  useEffect(() => {
    if (isLoggedIn) navigate("/app/dashboard", { replace: true });
  }, [navigate, isLoggedIn]);

  return (
    <Page className={classes.root}>
      <Box
        display="flex"
        flexDirection="column"
        height="100%"
        justifyContent="center"
      >
        <Container maxWidth="sm">
          <Formik
            initialValues={{
              email: "",
              password: "",
            }}
            validationSchema={Yup.object().shape({
              email: Yup.string()
                .email("Must be a valid email")
                .max(255)
                .required("Email is required"),
              password: Yup.string().max(255).required("Password is required"),
            })}
            onSubmit={(values, actions) => {
              postLogin(values, actions);
            }}
          >
            {({
              errors,
              handleBlur,
              handleChange,
              handleSubmit,
              isSubmitting,
              touched,
              values,
            }) => (
              <form onSubmit={handleSubmit}>
                <Box mb={3}>
                  <Typography color="textPrimary" variant="h2">
                    Sign in
                  </Typography>
                </Box>
                <TextField
                  error={Boolean(touched.email && errors.email)}
                  fullWidth
                  helperText={touched.email && errors.email}
                  label="Email Address"
                  margin="normal"
                  name="email"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  type="email"
                  value={values.email}
                  variant="outlined"
                />
                <TextField
                  error={Boolean(touched.password && errors.password)}
                  fullWidth
                  helperText={touched.password && errors.password}
                  label="Password"
                  margin="normal"
                  name="password"
                  onBlur={handleBlur}
                  onChange={handleChange}
                  type="password"
                  value={values.password}
                  variant="outlined"
                />
                {error ? (
                  <div className={classes.errorMessage}>{error}</div>
                ) : null}
                <Box my={2}>
                  <Button
                    color="primary"
                    disabled={isSubmitting}
                    fullWidth
                    size="large"
                    type="submit"
                    variant="contained"
                  >
                    Sign in
                  </Button>
                </Box>
              </form>
            )}
          </Formik>
        </Container>
      </Box>
    </Page>
  );
};

export default LoginView;
