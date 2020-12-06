import { v4 as uuid } from "uuid";

const cars = [
  {
    id: uuid(),
    modelName: "FIAT 500",
    media: "/static/images/cars/car_1.png",
    fuelType: "PETROL",
    gearboxType: "AUTO",
    acType: "AUTO",
    numberOfPassengers: 4,
    pricePerDay: 300.00,
    depositAmount: 1000.00
  },
  {
    id: uuid(),
    modelName: "HYUNDAI I20",
    media: "/static/images/cars/car_2.png",
    fuelType: "PETROL",
    gearboxType: "AUTO",
    acType: "AUTO",
    numberOfPassengers: 4,
    pricePerDay: 300.00,
    depositAmount: 1000.00
  },
  {
    id: uuid(),
    modelName: "VOLKSWAGEN POLO",
    media: "/static/images/cars/car_3.png",
    fuelType: "PETROL",
    gearboxType: "AUTO",
    acType: "AUTO",
    numberOfPassengers: 4,
    pricePerDay: 300.00,
    depositAmount: 1000.00
  },
  {
    id: uuid(),
    modelName: "TOYOTA COROLLA",
    media: "/static/images/cars/car_4.png",
    fuelType: "PETROL",
    gearboxType: "AUTO",
    acType: "AUTO",
    numberOfPassengers: 4,
    pricePerDay: 300.00,
    depositAmount: 1000.00
  },
  {
    id: uuid(),
    modelName: "RENAULT MASTER",
    media: "/static/images/cars/car_5.png",
    fuelType: "PETROL",
    gearboxType: "AUTO",
    acType: "AUTO",
    numberOfPassengers: 4,
    pricePerDay: 300.00,
    depositAmount: 1000.00
  },
  {
    id: uuid(),
    modelName: "MERCEDES E220",
    media: "/static/images/cars/car_6.png",
    fuelType: "PETROL",
    gearboxType: "AUTO",
    acType: "AUTO",
    numberOfPassengers: 4,
    pricePerDay: 300.00,
    depositAmount: 1000.00
  }
];

export default cars;
