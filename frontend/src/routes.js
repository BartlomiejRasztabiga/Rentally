import React from "react";
import { Navigate } from "react-router-dom";

import DashboardLayout from "src/layouts/DashboardLayout";
import MainLayout from "src/layouts/MainLayout";
import CustomerListView from "src/views/customer/CustomerListView";
import DashboardView from "src/views/dashboard/DashboardView";
import LoginView from "src/views/auth/LoginView";
import NotFoundView from "src/views/errors/NotFoundView";
import CarsListView from "src/views/cars/CarsListView";
import RegisterView from "src/views/auth/RegisterView";
import SettingsView from "src/views/settings/SettingsView";
import CarDetailsView from "src/views/cars/CarDetailsView";
import CreateCarView from "src/views/cars/CreateCarView";

const routes = [
  {
    path: "app",
    element: <DashboardLayout />,
    children: [
      { path: "customers", element: <CustomerListView /> },
      { path: "dashboard", element: <DashboardView /> },
      { path: "cars", element: <CarsListView /> },
      { path: "cars/new", element: <CreateCarView /> },
      { path: "cars/:carId", element: <CarDetailsView /> },
      { path: "settings", element: <SettingsView /> },
      { path: "*", element: <Navigate to="/404" /> }
    ]
  },
  {
    path: "/",
    element: <MainLayout />,
    children: [
      { path: "login", element: <LoginView /> },
      { path: "register", element: <RegisterView /> },
      { path: "404", element: <NotFoundView /> },
      { path: "/", element: <Navigate to="/app/dashboard" /> },
      { path: "*", element: <Navigate to="/404" /> }
    ]
  }
];

export default routes;
