import apiClient from "./client";

export const submitTraining = async (data) => {
  const response = await apiClient.post("/train", data);
  return response.data;
};