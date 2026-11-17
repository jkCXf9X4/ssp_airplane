within AircraftCommon;

partial model FuelSystem_Interface
  parameter Real fuel_capacity_kg = 3160;
  parameter Real reserve_fraction = 0.08;
  parameter Real fuelCapacityKg = 3160;
  parameter Real reserveFraction = 0.08;
  input GeneratedInterfaces.FuelConsumptionRate fuel_consumption_rate;
  output GeneratedInterfaces.FuelLevelState fuelState;
end FuelSystem_Interface;
