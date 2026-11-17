within AircraftCommon;

partial model TurbofanPropulsion_Interface
  parameter Real maxThrust_kN = 129.7;
  parameter Real dryThrust_kN = 79;
  parameter Real fuelEfficiency = 0.33;
  parameter Real fuelFlowAtFull_kgps = 1.15;
  parameter Real generatorOutputKW = 80;
  input GeneratedInterfaces.ThrottleCommand throttleCmd;
  output GeneratedInterfaces.ThrustState thrustOut;
  output GeneratedInterfaces.FuelConsumptionRate fuel_consumption;
end TurbofanPropulsion_Interface;
