import axiosInstance from "./instance";

const getUser = async () => {
    const user = await axiosInstance
        .get(userUrl)
        .then(response => response.data)
    return user;
}