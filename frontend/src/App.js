import "react-perfect-scrollbar/dist/css/styles.css";
import React from "react";
import { useRoutes } from "react-router-dom";
import { ThemeProvider } from "@material-ui/core";
import GlobalStyles from "./components/GlobalStyles";
import theme from "./theme";
import routes from "./routes";
import { AuthContext } from "./context/auth";

const App = () => {
  const routing = useRoutes(routes);

  return (
    <AuthContext.Provider value={false}>
      <ThemeProvider theme={theme}>
        <GlobalStyles />
        {routing}
      </ThemeProvider>
    </AuthContext.Provider>
  );
};

export default App;
