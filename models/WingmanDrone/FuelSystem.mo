within WingmanDrone;
model FuelSystem
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real fuelCapacityKg = 2000 "Total available fuel mass (kg)";
  parameter Real reserveFraction(min=0, max=0.5) = 0.05 "Unusable reserve fraction";
  Interfaces.RealInput fuelFlowIn "Fuel mass flow drawn by propulsion (kg/s)";
  Interfaces.RealOutput fuelState "Normalized fuel level (0..1)";
protected
  parameter Real reserveKg = reserveFraction * fuelCapacityKg;
  Real availableFuelKg(start=fuelCapacityKg, min=0);
  Real normalizedLevel;
equation
  der(availableFuelKg) = -max(0, fuelFlowIn);
  normalizedLevel = max(0, availableFuelKg - reserveKg) / max(1e-3, fuelCapacityKg - reserveKg);
  fuelState = max(0, min(1, normalizedLevel));
end FuelSystem;
