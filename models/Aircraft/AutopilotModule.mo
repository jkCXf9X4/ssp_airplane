within Aircraft;
model AutopilotModule
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real updateRateHz = 40;
  parameter Real sensorFidelity = 0.98;
  parameter Real defaultThrottle = 0.7;
  parameter Real headingGain = 1 / 60.0 "deg^-1 to normalize yaw error into stick roll";
  parameter Real altitudeGain = 1 / 3000.0 "m^-1 to normalize altitude error into stick pitch";
  parameter Real targetAltitude_m = 6000;
  input GI.FlightStatusPacket feedbackBus;
  input GI.GeodeticLLA currentLocation;
  input GI.OrientationEuler currentOrientation;
  output GI.PilotCommand autopilotCmd;
  output GI.MissionStatus missionStatus;
protected
  Real headingError;
  Real altitudeError;
  Real holdStrength;
  Real targetHeading;
equation
  // Simple stabilizer that nudges toward a nominal heading and altitude
  targetHeading = 0;
  headingError = targetHeading - currentOrientation.yaw_deg;
  altitudeError = targetAltitude_m - currentLocation.altitude_m;
  holdStrength = max(0.2, min(1.0, defaultThrottle * sensorFidelity * max(0.2, feedbackBus.energy_state_norm)));

  missionStatus.total_waypoints = 1;
  missionStatus.waypoint_index = 1;
  missionStatus.distance_to_waypoint_km = 0;
  missionStatus.arrived = true;
  missionStatus.complete = false;

  autopilotCmd.stick_roll_norm = max(-1.0, min(1.0, headingGain * headingError));
  autopilotCmd.rudder_norm = autopilotCmd.stick_roll_norm / 2;
  autopilotCmd.stick_pitch_norm = max(-1.0, min(1.0, altitudeGain * altitudeError));
  autopilotCmd.throttle_norm = holdStrength;
  autopilotCmd.throttle_aux_norm = autopilotCmd.throttle_norm;
  autopilotCmd.button_mask = 0;
  autopilotCmd.hat_x = 0;
  autopilotCmd.hat_y = 0;
  autopilotCmd.mode_switch = 1;
  autopilotCmd.reserved = 0;
end AutopilotModule;
