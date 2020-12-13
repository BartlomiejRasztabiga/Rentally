import axios from "./axios";
import { CARS_URL } from "../config";

const getCars = async () => {
  return await axios.get(CARS_URL).then(response => response.data);
};

const getCarById = async (carId) => {
  return await axios.get(`${CARS_URL}/${carId}`).then(response => response.data);
};

const updateCar = async (car) => {
  return await axios.put(`${CARS_URL}/${car.id}`, car).then(response => response.data)
}

const deleteCar = async (carId) => {
  return await axios.delete(`${CARS_URL}/${carId}`).then(response => response.data)
}

export { getCars, getCarById, updateCar, deleteCar };
