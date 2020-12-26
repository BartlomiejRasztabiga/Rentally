import axios from "./axios";
import { ACCESS_TOKEN_URL } from "../config";

const getAccessToken = async (username, password) => {
  const bodyFormData = new FormData();
  bodyFormData.append("username", username);
  bodyFormData.append("password", password);

  return await axios({
    method: "post",
    url: ACCESS_TOKEN_URL,
    data: bodyFormData,
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export { getAccessToken };
