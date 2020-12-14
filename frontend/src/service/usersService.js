import axios from "./axios";
import { GET_ME_URL } from "../config";

const getMe = async () => {
  return await axios.get(GET_ME_URL);
};

export { getMe };
