import axios from "axios";

export const getSourceOrders = async () => {
    const response = await axios.get("http://localhost:8000/source-orders");
    return response;
}

export const deleteSourceOrder = async (id) => {
    await axios.delete(`http://localhost:8000/source-order/${id}`);
}

export const postSourceOrder = async (name) => {
    const response = await axios
        .post("http://localhost:8000/source-order", { name: name })
    return response;
}