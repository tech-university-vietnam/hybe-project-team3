import axios from "axios";
import useAuth from "../hooks/auth"

export default {
    setupInterceptors: (history) => {
        axios.interceptors.request.use(
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
        
        axios.interceptors.response.use((response) => {
            return response
        }, async function (error) {
            if (error.response.status === 401) {
                localStorage.clear();
                history.go('/login');
            }
            return Promise.reject(error);
        });
    }
}