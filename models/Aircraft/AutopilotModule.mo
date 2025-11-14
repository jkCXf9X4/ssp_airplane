within Aircraft;
model AutopilotModule
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real updateRateHz = 40;
  parameter Real sensorFidelity = 0.98;
  parameter Real targetAltitude_m = 6000;
  input GI.FlightStatusPacket feedbackBus;
  input GI.GenericElectricalBus powerIn;
  input GI.GenericElectricalBus backupPower;
  input GI.AirDataInertialState airDataIn;
  input GI.StructuralPerformanceState performanceStatus;
  output GI.AutonomyGuidance guidanceCmd;
protected
  Real stability;
  Real altitudeError;
  Real holdStrength;
  Real performanceMargin;
equation
  holdStrength = min(1.0, max(0.3, (powerIn.available_power_kw + 0.3 * backupPower.available_power_kw) / 60.0));
  performanceMargin = max(0.4, performanceStatus.structural_margin_norm);
  stability = holdStrength * sensorFidelity * max(0.25, feedbackBus.energy_state_norm) * performanceMargin;
  altitudeError = targetAltitude_m - airDataIn.pressure_altitude_m;
  guidanceCmd.waypoint_heading_deg = 90 + 45 * sin(time / 30) + airDataIn.sideslip_deg;
  guidanceCmd.waypoint_altitude_m = targetAltitude_m + altitudeError * 0.2;
  guidanceCmd.lateral_accel_mps2 = min(30, max(5, feedbackBus.airspeed_mps / 10)) * performanceMargin;
  guidanceCmd.aggressiveness_norm = min(1.0, max(0.1, stability));
end AutopilotModule;
