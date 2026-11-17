within AircraftCommon;

partial model TurbofanPropulsion_Interface
  parameter Real max_thrust_kn = 129.7;
  parameter Real dry_thrust_kn = 79;
  parameter Real specific_fuel_consumption = 0.76;
  parameter Real fuel_capacity_kg = 3160;
  parameter Real generator_output_kw = 80;
  parameter Real maxThrust_kN = 129.7;
  parameter Real dryThrust_kN = 79;
  parameter Real generatorOutputKW = 80;
  parameter Real fuelEfficiency = 0.33;
  parameter Real fuelFlowAtFull_kgps = 1.15;
  input GeneratedInterfaces.ThrottleCommand throttleCmd;
  output GeneratedInterfaces.ThrustState thrustOut;
  output GeneratedInterfaces.FuelConsumptionRate fuel_consumption;
end TurbofanPropulsion_Interface;
