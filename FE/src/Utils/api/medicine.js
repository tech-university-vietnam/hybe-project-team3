import axios from "axios";

export const getTrackingMedicines = async () => {
  const response = await axios.get("http://localhost:8000/tracking-medicines");
  return response;
};

export const deleteTrackingMedicine = async (id) => {
  await axios.delete(`http://localhost:8000/tracking-medicine/${id}`);
};

export const postTrackingMedicine = async (name, date) => {
  const response = await axios.post("http://localhost:8000/tracking-medicine", {
    name: name,
    expired_date: date,
    number: 0,
  });
  return response;
};

export const getBuyingHospital = async (id) => {
    const response = await axios.get(`http://localhost:8000/tracking-medicine/${id}`)
    return response
};

