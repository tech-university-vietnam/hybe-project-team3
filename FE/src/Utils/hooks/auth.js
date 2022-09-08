import axios from "axios";
import * as React from "react";

const authContext = React.createContext();

function useAuth() {
    const [authed, setAuthed] = React.useState(null);
    const [isLoading, setIsLoading] = React.useState(true);
    const loginUrl = "http://localhost:8000/login";
    const logoutUrl = "http://localhost:8000/logout";
    const userUrl = "http://localhost:8000/user";

    React.useEffect(() => {
        const getAuthedByToken = async (token) => {
            const email = await getEmail(token);
            setAuthed(email);
            setIsLoading(false);
        }

        const token = localStorage.getItem("token");
        if (token) {
            getAuthedByToken(token);
        } else {
            setAuthed(null);
            setIsLoading(false);
        }
    }, []);

    const getEmail = async (token) => {
        return axios.get(userUrl, { headers: { Authorization: `Bearer ${token}` } })
            .then(response => response.data)
            .then(response => response.email)
            .catch(() => null);
    }

    return {
        authed,
        isLoading,
        login(data) {
            return axios
                .post(loginUrl, data)
                .then((response) => {
                    setAuthed(data.email);
                    localStorage.setItem("token", response.data.token);
                });
        },
        logout() {
            let token = localStorage.getItem("token");
            return axios
                .post(logoutUrl, { email: authed }, { headers: { Authorization: `Bearer ${token}` } })
                .then(() => {
                    localStorage.removeItem("token");
                    setAuthed(null);
                })
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