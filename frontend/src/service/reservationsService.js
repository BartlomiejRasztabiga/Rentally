import axios from "./axios";
import { RESERVATIONS_URL } from "../config";
import cleanupFalsyFields from "../utils/cleanupFalsyFields";

const getReservations = async () => {
  return await axios
    .get(`${RESERVATIONS_URL}/`)
    .then((response) => response.data);
};

const getReservationById = async (reservationId) => {
  return await axios
    .get(`${RESERVATIONS_URL}/${reservationId}`)
    .then((response) => response.data);
};

const createReservation = async (reservation) => {
  reservation.status = "NEW";
  return await axios
    .post(`${RESERVATIONS_URL}/`, cleanupFalsyFields(reservation))
    .then((response) => response.data);
};

const updateReservation = async (reservation) => {
  reservation.status = null;
  return await axios
    .put(
      `${RESERVATIONS_URL}/${reservation.id}`,
      cleanupFalsyFields(reservation)
    )
    .then((response) => response.data);
};

const deleteReservation = async (reservationId) => {
  return await axios
    .delete(`${RESERVATIONS_URL}/${reservationId}`)
    .then((response) => response.data);
};

export {
  getReservations,
  getReservationById,
  updateReservation,
  deleteReservation,
  createReservation,
};
