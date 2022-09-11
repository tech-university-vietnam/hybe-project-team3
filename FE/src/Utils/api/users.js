import axios from "axios";

export const getUser = async () => {
    const user = await axios
        .get("http://localhost:8000/user")
        .then(response => response.data)
    return user;
}

export const login = async (data) => {
    const response = await axios
        .post("http://localhost:8000/login", data)
    return response
}

