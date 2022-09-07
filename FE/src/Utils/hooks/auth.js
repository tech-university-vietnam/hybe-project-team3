import axios from "axios";
import * as React from "react";

const authContext = React.createContext();

function useAuth() {
    const [authed, setAuthed] = React.useState(false);
    const [email, setEmail] = React.useState('');
    const loginUrl = "http://localhost:8000/login";
    const logoutUrl = "http://localhost:8000/logout";

    React.useEffect(() => {
    }, []);

    return {
        authed,
        email,
        login(data) {
            return axios
                .post(loginUrl, data)
                .then((response) => {
                    setAuthed(true);
                    setEmail(data.email);
                    localStorage.setItem("token", response.data.token);
                });
        },
        logout() {
            let token = localStorage.getItem("token");
            return axios
                .post(logoutUrl, { email: email }, { headers: { Authorization: `Bearer ${token}` } })
                .then((response) => localStorage.removeItem("token"))
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