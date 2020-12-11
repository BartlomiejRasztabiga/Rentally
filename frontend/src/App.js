import "react-perfect-scrollbar/dist/css/styles.css";
import React, { useState } from "react";
import { useRoutes } from "react-router-dom";
import { ThemeProvider } from "@material-ui/core";
import GlobalStyles from "./components/GlobalStyles";
import theme from "./theme";
import routes from "./routes";
import { AuthContext } from "./context/auth";

const App = () => {
  const routing = useRoutes(routes);
  const [accessToken, setAccessTokenState] = useState(localStorage.getItem("access_token"));

  const setAccessToken = (data) => {
    if (!data) {
      localStorage.removeItem("access_token");
      setAccessTokenState(null);
    } else {
      localStorage.setItem("access_token", JSON.stringify(data));
      setAccessTokenState(data);
    }
  };

  return (
    <AuthContext.Provider value={{ accessToken, setAccessToken }}>
      <ThemeProvider theme={theme}>
        <GlobalStyles />
        {routing}
      </ThemeProvider>
    </AuthContext.Provider>
  );
};

export default App;
