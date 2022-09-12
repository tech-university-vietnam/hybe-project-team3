import axios from "axios";

export const getNotSeenNotifications = async () => {
  const response = await axios.get(
    "http://localhost:8000/notification/not-seen"
  );
  return response;
};

export const getAllNotifications = async () => {
  const response = await axios.get("http://localhost:8000/notifications");
  return response;
};

export const postApproveNotification = async ({ id }) => {
  await axios.post(`http://localhost:8000/notification/${id}/approved`);
};

export const postDeclineNotification = async ({ id }) => {
  await axios.post(`http://localhost:8000/notification/${id}/declined`);
};
