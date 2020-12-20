import axios from "./axios";
import { CARS_URL } from "../config";
import cleanupFalsyFields from "../utils/cleanupFalsyFields";

const mapRangeCriterion = (range) => {
  return range[0] && range[1] ? { start: range[0], end: range[1] } : null;
};

const mapAvailabilityDates = (startDate, endDate) => {
  return startDate && endDate ? { start: startDate, end: endDate } : null;
};

const mapSearchQuery = (search_query) => {
  let query_data = Object.assign({}, search_query);
  query_data = cleanupFalsyFields(query_data);
  return {
    model_name: query_data.model_name,
    type: query_data.type,
    fuel_type: query_data.fuel_type,
    gearbox_type: query_data.gearbox_type,
    ac_type: query_data.ac_type,
    drive_type: query_data.drive_type,
    number_of_passengers: mapRangeCriterion(query_data.number_of_passengers),
    price_per_day: mapRangeCriterion(query_data.price_per_day),
    availability_dates: mapAvailabilityDates(
      query_data.start_date,
      query_data.end_date
    ),
  };
};

const getCars = async () => {
  return await axios.get(`${CARS_URL}/`).then((response) => response.data);
};

const getCarsWithSearchQuery = async (search_query) => {
  return await axios
    .post(`${CARS_URL}/query`, mapSearchQuery(search_query))
    .then((response) => response.data);
};

const getCarById = async (carId) => {
  return await axios
    .get(`${CARS_URL}/${carId}`)
    .then((response) => response.data);
};

const createCar = async (car) => {
  return await axios
    .post(`${CARS_URL}/`, cleanupFalsyFields(car))
    .then((response) => response.data);
};

const updateCar = async (car) => {
  return await axios
    .put(`${CARS_URL}/${car.id}`, cleanupFalsyFields(car))
    .then((response) => response.data);
};

const deleteCar = async (carId) => {
  return await axios
    .delete(`${CARS_URL}/${carId}`)
    .then((response) => response.data);
};

export {
  getCars,
  getCarById,
  updateCar,
  deleteCar,
  createCar,
  getCarsWithSearchQuery,
};
