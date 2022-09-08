import axios from "axios";

export const postRegister = async (data) => {
    await axios.post("http://localhost:8000/register", {
        email: data.email,
        password: data.password,
        work_for: data.hospital,
    }).then(response => response.data).catch();
}

export const logout = async (data) => {
    await axios.post("http://localhost:8000/logout", data)
}