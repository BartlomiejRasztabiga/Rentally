import axios from "./axios";
import { RENTALS_URL } from "../config";
import cleanupFalsyFields from "../utils/cleanupFalsyFields";

const getRentals = async () => {
  return await axios.get(`${RENTALS_URL}/`).then((response) => response.data);
};

const getOvertimeRentals = async () => {
  return await axios
    .get(`${RENTALS_URL}/overtime`)
    .then((response) => response.data);
};

const getRentalById = async (rentalId) => {
  return await axios
    .get(`${RENTALS_URL}/${rentalId}`)
    .then((response) => response.data);
};

const createRental = async (rental) => {
  rental.status = "IN_PROGRESS";
  return await axios
    .post(`${RENTALS_URL}/`, cleanupFalsyFields(rental))
    .then((response) => response.data);
};

const updateRental = async (rental) => {
  return await axios
    .put(`${RENTALS_URL}/${rental.id}`, cleanupFalsyFields(rental))
    .then((response) => response.data);
};

const updateRentalStatus = async (rental, newStatus) => {
  rental.status = newStatus;
  return await updateRental(rental);
};

const deleteRental = async (rentalId) => {
  return await axios
    .delete(`${RENTALS_URL}/${rentalId}`)
    .then((response) => response.data);
};

export {
  getRentals,
  getRentalById,
  updateRental,
  deleteRental,
  createRental,
  updateRentalStatus,
  getOvertimeRentals,
};
