within Aircraft;
model TurbofanPropulsion
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real maxThrust_kN = 129.7;
  parameter Real dryThrust_kN = 79.0;
  parameter Real generatorOutputKW = 80;
  parameter Real fuelEfficiency = 0.33;
  parameter Real fuelFlowAtFull_kgps = 1.15;
  input GI.ThrottleCommand throttleCmd;
  output GI.ThrustState thrustOut;
  output GI.FuelConsumptionRate fuel_consumption;
protected
  Real commandedThrust;
  Real throttle;
equation
  throttle = max(0, min(1, throttleCmd.throttle_norm)) * (if throttleCmd.fuel_enable then 1 else 0);
  commandedThrust = throttle * (dryThrust_kN + (maxThrust_kN - dryThrust_kN) * (if throttleCmd.afterburner_enable then 1 else throttle));
  thrustOut.thrust_kn = commandedThrust;
  thrustOut.mass_flow_kgps = throttle * fuelFlowAtFull_kgps;
  thrustOut.exhaust_velocity_mps = 350 + 150 * throttle;
  fuel_consumption.mass_flow_kgps = thrustOut.mass_flow_kgps;
end TurbofanPropulsion;
