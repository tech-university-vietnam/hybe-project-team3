import axios from "axios";

export const getHospitals = async () => {
    const response = await axios.get('http://localhost:8000/hospitals')
        .then(response => response.data)
    return response
}