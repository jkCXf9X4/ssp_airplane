within Aircraft;
model AutopilotModule
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real updateRateHz = 40;
  parameter Real sensorFidelity = 0.98;
  parameter Real targetAltitude_m = 6000;
  parameter Integer waypointCount = 10;
  parameter Real waypointLat[waypointCount] = fill(0.0, waypointCount);
  parameter Real waypointLon[waypointCount] = fill(0.0, waypointCount);
  parameter Real waypointAlt[waypointCount] = fill(targetAltitude_m, waypointCount);
  parameter Real waypointProximity_km = 10 "Distance to trigger waypoint switch";
  parameter Real cumulativeSwitch_km[waypointCount - 1] = fill(100.0, waypointCount - 1);
  parameter Real pathSpeedScale = 3.0;
  input GI.FlightStatusPacket feedbackBus;
  input GI.GenericElectricalBus powerIn;
  input GI.GenericElectricalBus backupPower;
  input GI.AirDataInertialState airDataIn;
  input GI.StructuralPerformanceState performanceStatus;
  input GI.GeodeticLLA currentLocation;
  input GI.OrientationEuler currentOrientation;
  output GI.AutonomyGuidance guidanceCmd;
  output GI.PilotCommand autopilotCmd;
  output GI.MissionStatus missionStatus;
protected
  Integer waypointIndex;
  Boolean missionDone;
  Real targetLat(start=0);
  Real targetLon(start=0);
  Real targetAlt(start=0);
  Real deltaLat(start=0);
  Real deltaLon(start=0);
  Real distanceKm(start=10);
  Real bearingDeg(start=0);
  Real headingError(start=0);
  Real altitudeError(start=0);
  Real stability;
  Real holdStrength;
  Real performanceMargin;
  Real travelKm;
equation
  holdStrength = min(1.0, max(0.3, (powerIn.available_power_kw + 0.3 * backupPower.available_power_kw) / 60.0));
  performanceMargin = max(0.4, performanceStatus.structural_margin_norm);
  stability = holdStrength * sensorFidelity * max(0.25, feedbackBus.energy_state_norm) * performanceMargin;
  travelKm = time * feedbackBus.airspeed_mps * pathSpeedScale / 1000.0;
  waypointIndex = min(waypointCount, 1 + sum({if travelKm >= cumulativeSwitch_km[i] then 1 else 0 for i in 1:(waypointCount - 1)}));
  targetLat = if waypointCount > 0 then waypointLat[waypointIndex] else currentLocation.latitude_deg;
  targetLon = if waypointCount > 0 then waypointLon[waypointIndex] else currentLocation.longitude_deg;
  targetAlt = if waypointCount > 0 then waypointAlt[waypointIndex] else targetAltitude_m;

  deltaLat = targetLat - currentLocation.latitude_deg;
  deltaLon = targetLon - currentLocation.longitude_deg;
  distanceKm = max(1e-3, 111.0 * sqrt(
    (deltaLat) ^ 2 +
    (cos(currentLocation.latitude_deg * 3.14159265358979 / 180) * (deltaLon)) ^ 2));
  bearingDeg = if distanceKm < 1e-3 then currentOrientation.yaw_deg else atan2(deltaLon, deltaLat) * 180 / 3.14159265358979;
  headingError = bearingDeg - currentOrientation.yaw_deg;
  altitudeError = targetAlt - currentLocation.altitude_m;

  missionDone = waypointIndex >= waypointCount;

  missionStatus.total_waypoints = waypointCount;
  missionStatus.waypoint_index = waypointIndex;
  missionStatus.distance_to_waypoint_km = distanceKm;
  missionStatus.arrived = distanceKm < waypointProximity_km;
  missionStatus.complete = missionDone;

  guidanceCmd.waypoint_heading_deg = bearingDeg;
  guidanceCmd.waypoint_altitude_m = targetAlt;
  guidanceCmd.lateral_accel_mps2 = min(30, max(5, feedbackBus.airspeed_mps / 10)) * performanceMargin;
  guidanceCmd.aggressiveness_norm = min(1.0, max(0.1, stability));

  autopilotCmd.stick_roll_norm = max(-1.0, min(1.0, headingError / 45));
  autopilotCmd.rudder_norm = autopilotCmd.stick_roll_norm / 2;
  autopilotCmd.stick_pitch_norm = max(-1.0, min(1.0, altitudeError / 2000));
  autopilotCmd.throttle_norm = min(1.0, max(0.2, holdStrength * (0.6 + performanceMargin / 2)));
  autopilotCmd.throttle_aux_norm = autopilotCmd.throttle_norm;
  autopilotCmd.button_mask = 0;
  autopilotCmd.hat_x = 0;
  autopilotCmd.hat_y = 0;
  autopilotCmd.mode_switch = if missionDone then 0 else 1;
  autopilotCmd.reserved = waypointIndex;
end AutopilotModule;
