import axios from "./axios";
import { CUSTOMERS_URL } from "../config";
import cleanupFalsyFields from "../utils/cleanupFalsyFields";


const getCustomers = async () => {
  return await axios.get(`${CUSTOMERS_URL}/`).then(response => response.data);
};

const getCustomerById = async (customerId) => {
  return await axios.get(`${CUSTOMERS_URL}/${customerId}`).then(response => response.data);
};

const createCustomer = async (customer) => {
  return await axios.post(`${CUSTOMERS_URL}/`, cleanupFalsyFields(customer)).then(response => response.data);
};

const updateCustomer = async (customer) => {
  return await axios.put(`${CUSTOMERS_URL}/${customer.id}`, cleanupFalsyFields(customer)).then(response => response.data);
};

const deleteCustomer = async (customerId) => {
  return await axios.delete(`${CUSTOMERS_URL}/${customerId}`).then(response => response.data);
};

export { getCustomers, getCustomerById, updateCustomer, deleteCustomer, createCustomer };
