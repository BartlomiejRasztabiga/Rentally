import axios from "axios";
import { GET_ME_URL } from "../config";

const getMe = async accessToken => {
  return await axios.get(GET_ME_URL, {
    headers: {
      Authorization: "Bearer " + accessToken
    }
  })
};

export { getMe };
