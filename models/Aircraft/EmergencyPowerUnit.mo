within Aircraft;
model EmergencyPowerUnit
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real durationMinutes = 10;
  parameter Real generatorOutputKW = 25;
  parameter Real nominalVoltageKV = 0.27;
  input GI.FuelLevelState fuelState;
  output GI.GenericElectricalBus emergencyOutput;
protected
  Real activationLevel;
  Real enduranceScalar;
equation
  enduranceScalar = max(0.2, min(1.0, durationMinutes / 10));
  activationLevel = if fuelState.fuel_starved then 1 else min(1.0, max(0.0, 1 - fuelState.fuel_level_norm));

  emergencyOutput.available_power_kw = generatorOutputKW * activationLevel * enduranceScalar;
  emergencyOutput.voltage_kv = nominalVoltageKV;
  emergencyOutput.current_a = if nominalVoltageKV > 1e-6 then emergencyOutput.available_power_kw * 1000 / (nominalVoltageKV * 1000) else 0;
end EmergencyPowerUnit;
