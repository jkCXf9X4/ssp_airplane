within Aircraft;
model FuelSystem
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real fuelCapacityKg = 3160 "Total available fuel mass (kg)";
  parameter Real reserveFraction(min=0, max=0.5) = 0.08 "Unusable reserve fraction";
  input GI.FuelConsumptionRate fuel_consumption_rate "Fuel mass flow drawn by propulsion (kg/s)";
  output GI.FuelLevelState fuelState "Remaining fuel telemetry";
protected
  parameter Real reserveKg = reserveFraction * fuelCapacityKg;
  Real availableFuelKg(start=fuelCapacityKg, min=0);
  Real normalizedLevel;
equation
  der(availableFuelKg) = -max(0, fuel_consumption_rate.mass_flow_kgps);
  normalizedLevel = max(0, availableFuelKg - reserveKg) / max(1e-3, fuelCapacityKg - reserveKg);
  fuelState.fuel_remaining_kg = availableFuelKg;
  fuelState.fuel_level_norm = max(0, min(1, normalizedLevel));
  fuelState.fuel_starved = fuelState.fuel_level_norm <= 0.01;
end FuelSystem;
