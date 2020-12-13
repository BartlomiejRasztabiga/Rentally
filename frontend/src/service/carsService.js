import axios from "./axios";
import { GET_ALL_CARS } from "../config";

const getCars = async () => {
  return await axios.get(GET_ALL_CARS).then(response => response.data);
};

export { getCars };
