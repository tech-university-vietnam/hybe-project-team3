import axios from "axios";
import * as React from "react";
import { login, getUser } from "Utils/api/users";
import { logout } from "Utils/api/authentication";

const authContext = React.createContext();

function useAuth() {
    const [authed, setAuthed] = React.useState(null);
    const [isLoading, setIsLoading] = React.useState(true);
    
    React.useEffect(() => {
        const getAuthed = async () => {
            if (localStorage.getItem("token") === null) {
                setAuthed(null);
            } else {
                const email = await getUser()
                    .then(response => response.email)
                    .catch(() => null);
                setAuthed(email);
            }
            setIsLoading(false);
        }

        getAuthed();
    }, []);

    return {
        authed,
        isLoading,
        login(data) {
            return login(data)
                .then((response) => {
                    setAuthed(data.email);
                    localStorage.setItem("token", response.data.token);
                });
        },
        logout() {
            return logout({ email: authed })
                .then(() => {
                    localStorage.removeItem("token");
                    setAuthed(null);
                })
        }
    };
}

export function AuthProvider({ children }) {
    const auth = useAuth();

    return <authContext.Provider value={auth}>{children}</authContext.Provider>;
}

export default function AuthConsumer() {
    return React.useContext(authContext);
}