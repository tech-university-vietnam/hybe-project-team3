import axios from "axios";
import * as React from "react";

const authContext = React.createContext();

function useAuth() {
  const [authed, setAuthed] = React.useState(false);
  const loginUrl = "http://localhost:8000/login";

  return {
    authed,
    login(data) {
      return axios
      .post(loginUrl, data)
      .then((response) => {
        setAuthed(true)
        localStorage.setItem("token", response.data.token);
      });
    },
    logout() {
      return new Promise((res) => {
        setAuthed(false);
        res();
      });
    },
  };
}

export function AuthProvider({ children }) {
  const auth = useAuth();

  return <authContext.Provider value={auth}>{children}</authContext.Provider>;
}

export default function AuthConsumer() {
  return React.useContext(authContext);
}