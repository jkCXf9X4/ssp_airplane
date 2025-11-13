within WingmanDrone;
model TurbofanPropulsion
  import GI = WingmanDrone.GeneratedInterfaces;
  parameter Real maxThrust_kN = 60;
  parameter Real generatorOutputKW = 150;
  parameter Real fuelEfficiency = 0.38;
  parameter Real fuelFlowAtFull_kgps = 0.75;
  input GI.ThrottleCommand throttleCmd;
  input GI.FuelLevelState fuelStatus;
  output GI.ThrustState thrustOut;
  output GI.FuelConsumptionRate fuelFlow;
  output GI.ElectricalBusState powerBus;
protected
  Real commandedThrust;
  Real throttle;
  Real fuelAvailability;
equation
  throttle = max(0, min(1, throttleCmd.throttle_norm)) * (if throttleCmd.fuel_enable then 1 else 0);
  fuelAvailability = if fuelStatus.fuel_starved then 0 else max(0, min(1, fuelStatus.fuel_level_norm));
  commandedThrust = throttle * fuelAvailability * maxThrust_kN;
  thrustOut.thrust_kn = commandedThrust;
  thrustOut.mass_flow_kgps = throttle * fuelAvailability * fuelFlowAtFull_kgps;
  thrustOut.exhaust_velocity_mps = 300 + 100 * throttle;
  fuelFlow.mass_flow_kgps = thrustOut.mass_flow_kgps;
  powerBus.voltage_kv = generatorOutputKW / 1000;
  powerBus.current_a = 100 * throttle;
  powerBus.available_power_kw = generatorOutputKW * fuelEfficiency * max(0.2, throttle) * fuelAvailability;
end TurbofanPropulsion;
