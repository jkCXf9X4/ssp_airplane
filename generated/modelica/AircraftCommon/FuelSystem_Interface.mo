within AircraftCommon;

partial model FuelSystem_Interface
  parameter Real fuelCapacityKg = 3160;
  parameter Real reserveFraction = 0.08;
  input GeneratedInterfaces.FuelConsumptionRate fuel_consumption_rate;
  output GeneratedInterfaces.FuelLevelState fuelState;
end FuelSystem_Interface;
