within WingmanDrone;
model AutopilotModule
  import GI = WingmanDrone.GeneratedInterfaces;
  parameter Real updateRateHz = 25;
  parameter Real sensorFidelity = 0.95;
  input GI.FlightStatusPacket feedbackBus;
  input GI.GenericElectricalBus powerIn;
  output GI.AutonomyGuidance guidanceCmd;
protected
  Real stability;
equation
  stability = min(1.0, max(0.2, powerIn.available_power_kw / 100.0)) * sensorFidelity * max(0.2, feedbackBus.energy_state_norm);
  guidanceCmd.waypoint_heading_deg = 360 * stability;
  guidanceCmd.waypoint_altitude_m = 1000 + 500 * feedbackBus.angle_of_attack_deg;
  guidanceCmd.lateral_accel_mps2 = 2 * feedbackBus.airspeed_mps / 200;
  guidanceCmd.aggressiveness_norm = stability;
end AutopilotModule;
