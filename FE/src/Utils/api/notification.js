import axios from "axios";

export const getNotSeenNotifications = async () => {
  const response = await axios.get(
    "http://localhost:8000/notification/notseen"
  );
  return response;
};

export const getAllNotifications = async () => {
  const response = await axios.get("http://localhost:8000/notifications");
  return response;
};

export const postApproveNotification = async ({ id }) => {
  await axios.post("http://localhost:8000/notification/approved", { id: id });
};

export const postDeclineNotification = async ({ id }) => {
  await axios.post("http://localhost:8000/notification/declined", { id: id });
};
