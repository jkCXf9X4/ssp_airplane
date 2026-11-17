within TurbofanPropulsionFMU;
model TurbofanPropulsion
  extends AircraftCommon.TurbofanPropulsion_Interface;
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
