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
  const [accessToken, setAuthTokens] = useState(localStorage.getItem("access_token"));

  const setAccessToken = (data) => {
    localStorage.setItem("access_token", JSON.stringify(data));
    setAuthTokens(data);
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
