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
  search_query = cleanupFalsyFields(search_query);
  return {
    model_name: search_query.model_name,
    type: search_query.type,
    fuel_type: search_query.fuel_type,
    gearbox_type: search_query.gearbox_type,
    ac_type: search_query.ac_type,
    drive_type: search_query.drive_type,
    number_of_passengers: mapRangeCriterion(search_query.number_of_passengers),
    price_per_day: mapRangeCriterion(search_query.price_per_day),
    availability_dates: mapAvailabilityDates(
      search_query.start_date,
      search_query.end_date
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
