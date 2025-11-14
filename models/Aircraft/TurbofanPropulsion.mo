within Aircraft;
model TurbofanPropulsion
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real maxThrust_kN = 129.7;
  parameter Real dryThrust_kN = 79.0;
  parameter Real generatorOutputKW = 80;
  parameter Real fuelEfficiency = 0.33;
  parameter Real fuelFlowAtFull_kgps = 1.15;
  input GI.ThrottleCommand throttleCmd;
  input GI.FuelLevelState fuelStatus;
  output GI.ThrustState thrustOut;
  output GI.FuelConsumptionRate fuelFlow;
  output GI.GenericElectricalBus powerBus;
protected
  Real commandedThrust;
  Real throttle;
  Real fuelAvailability;
equation
  throttle = max(0, min(1, throttleCmd.throttle_norm)) * (if throttleCmd.fuel_enable then 1 else 0);
  fuelAvailability = if fuelStatus.fuel_starved then 0 else max(0, min(1, fuelStatus.fuel_level_norm));
  commandedThrust = throttle * fuelAvailability * (dryThrust_kN + (maxThrust_kN - dryThrust_kN) * (if throttleCmd.afterburner_enable then 1 else throttle));
  thrustOut.thrust_kn = commandedThrust;
  thrustOut.mass_flow_kgps = throttle * fuelAvailability * fuelFlowAtFull_kgps;
  thrustOut.exhaust_velocity_mps = 350 + 150 * throttle;
  fuelFlow.mass_flow_kgps = thrustOut.mass_flow_kgps;
  powerBus.voltage_kv = 0.27;
  powerBus.current_a = (generatorOutputKW * fuelEfficiency * max(0.2, throttle)) * 1000 / (powerBus.voltage_kv * 1000);
  powerBus.available_power_kw = generatorOutputKW * fuelEfficiency * max(0.2, throttle) * fuelAvailability;
end TurbofanPropulsion;
