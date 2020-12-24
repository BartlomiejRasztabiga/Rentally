import React from "react";
import { Navigate } from "react-router-dom";

import DashboardLayout from "./layouts/DashboardLayout";
import MainLayout from "./layouts/MainLayout";
import CustomersListView from "./views/customers/CustomerListView";
import CustomerDetailsView from "./views/customers/CustomerDetailsView";
import CreateCustomerView from "./views/customers/CreateCustomerView";
import DashboardView from "./views/dashboard/DashboardView";
import LoginView from "./views/auth/LoginView";
import NotFoundView from "./views/errors/NotFoundView";
import CarsListView from "./views/cars/CarsListView";
import RegisterView from "./views/auth/RegisterView";
import CarDetailsView from "./views/cars/CarDetailsView";
import CreateCarView from "./views/cars/CreateCarView";
import ReservationsListView from "./views/reservations/ReservationsListView";
import ReservationDetailsView from "./views/reservations/ReservationDetailsView";
import CreateReservationView from "./views/reservations/CreateReservationView";
import RentalsListView from "./views/rentals/RentalsListView";
import CreateRentalView from "./views/rentals/CreateRentalView";
import RentalDetailsView from "./views/rentals/RentalDetailsView";
import OvertimeRentalsListView from "./views/rentals/OvertimeRentalsListView";

const routes = [
  {
    path: "app",
    element: <DashboardLayout />,
    children: [
      { path: "dashboard", element: <DashboardView /> },

      { path: "cars", element: <CarsListView /> },
      { path: "cars/new", element: <CreateCarView /> },
      { path: "cars/:carId", element: <CarDetailsView /> },

      { path: "customers", element: <CustomersListView /> },
      { path: "customers/new", element: <CreateCustomerView /> },
      { path: "customers/:customerId", element: <CustomerDetailsView /> },

      { path: "reservations", element: <ReservationsListView /> },
      { path: "reservations/new", element: <CreateReservationView /> },
      {
        path: "reservations/:reservationId",
        element: <ReservationDetailsView />,
      },

      { path: "rentals", element: <RentalsListView /> },
      { path: "rentals/new", element: <CreateRentalView /> },
      { path: "rentals/overtime", element: <OvertimeRentalsListView /> },
      { path: "rentals/:rentalId", element: <RentalDetailsView /> },

      { path: "*", element: <Navigate to="/404" /> },
    ],
  },
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { path: "login", element: <LoginView /> },
      { path: "register", element: <RegisterView /> },
      { path: "404", element: <NotFoundView /> },
      { path: "/", element: <Navigate to="/app/dashboard" /> },
      { path: "*", element: <Navigate to="/404" /> },
    ],
  },
];

export default routes;
