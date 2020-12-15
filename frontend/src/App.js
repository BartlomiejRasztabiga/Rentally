import "react-perfect-scrollbar/dist/css/styles.css";
import React, { useEffect, useState } from "react";
import { useRoutes } from "react-router-dom";
import { ThemeProvider } from "@material-ui/core";
import { MuiPickersUtilsProvider } from "@material-ui/pickers";
import MomentUtils from '@date-io/moment';
import GlobalStyles from "./components/GlobalStyles";
import theme from "./theme";
import routes from "./routes";
import { AuthContext } from "./context/auth";
import { getMe } from "./service/usersService";

const App = () => {
  const routing = useRoutes(routes);
  const [accessToken, setAccessTokenState] = useState(
    localStorage.getItem("access_token")
  );

  // TODO can this be extracted to auth context?

  const setAccessToken = (data) => {
    if (!data) {
      localStorage.removeItem("access_token");
      setAccessTokenState(null);
    } else {
      localStorage.setItem("access_token", data);
      setAccessTokenState(data);
    }
  };

  useEffect(() => {
    // check if JWT is correct and not expired
    (async () => {
      if (accessToken) {
        try {
          await getMe(accessToken);
        } catch (e) {
          setAccessToken(null);
        }
      }
    })();
  }, [accessToken]);

  return (
    <AuthContext.Provider value={{ accessToken, setAccessToken }}>
      <MuiPickersUtilsProvider utils={MomentUtils}>
        <ThemeProvider theme={theme}>
          <GlobalStyles />
          {routing}
        </ThemeProvider>
      </MuiPickersUtilsProvider>
    </AuthContext.Provider>
  );
};

export default App;
