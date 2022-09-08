import axios from "axios";
import useAuth from "../hooks/auth"

const axiosInstance = axios.create();
const { requireLogin } = useAuth();

axiosInstance.interceptors.request.use(
    async config => {
        const token = localStorage.getItem("token");
        config.headers = {
            Authorization: `Bearer ${token}`
        }
        return config;
    },
    error => {
        Promise.reject(error)
    }
);

axiosInstance.interceptos.response.use((response) => {
    return response
}, async function (error) {
    if (error.response.status === 401) {
        requireLogin();
    }
    return Promise.reject(error);
});

export default axiosInstance