within Aircraft;
model AutopilotModule
  import GI = Aircraft.GeneratedInterfaces;
  import Modelica.Math;
  import Aircraft.stringToRealVector;
  parameter Real updateRateHz = 40;
  parameter Real sensorFidelity = 0.98;
  parameter Real targetAltitude_m = 6000;
  parameter String scenarioData = "0.0,0.0,1500.0, 0.2,0.1,2000.0, 0.4,0.2,1500.0";
  parameter Real waypointProximity_km = 5 "Distance to trigger waypoint switch";
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
  parameter Real scenarioValues[:] = stringToRealVector(scenarioData);
  parameter Integer waypointCount = integer(size(scenarioValues, 1) / 3);
  parameter Real waypointLat[waypointCount] = {scenarioValues[3 * i - 2] for i in 1:waypointCount};
  parameter Real waypointLon[waypointCount] = {scenarioValues[3 * i - 1] for i in 1:waypointCount};
  parameter Real waypointAlt[waypointCount] = {scenarioValues[3 * i] for i in 1:waypointCount};
  discrete Integer waypointIndex(start=1, fixed=true);
  Boolean missionDone(start=false, fixed=true);
  Real targetLat;
  Real targetLon;
  Real targetAlt;
  Real distanceKm;
  Real bearingDeg;
  Real headingError;
  Real altitudeError;
  Real stability;
  Real holdStrength;
  Real performanceMargin;
equation
  holdStrength = min(1.0, max(0.3, (powerIn.available_power_kw + 0.3 * backupPower.available_power_kw) / 60.0));
  performanceMargin = max(0.4, performanceStatus.structural_margin_norm);
  stability = holdStrength * sensorFidelity * max(0.25, feedbackBus.energy_state_norm) * performanceMargin;
  targetLat = if waypointCount > 0 then waypointLat[waypointIndex] else currentLocation.latitude_deg;
  targetLon = if waypointCount > 0 then waypointLon[waypointIndex] else currentLocation.longitude_deg;
  targetAlt = if waypointCount > 0 then waypointAlt[waypointIndex] else targetAltitude_m;

  distanceKm = 111.0 * sqrt(
    (targetLat - currentLocation.latitude_deg) ^ 2 +
    (cos(currentLocation.latitude_deg * 3.14159265358979 / 180) * (targetLon - currentLocation.longitude_deg)) ^ 2);
  bearingDeg = Math.atan2(targetLon - currentLocation.longitude_deg, targetLat - currentLocation.latitude_deg) * 180 / 3.14159265358979;
  headingError = bearingDeg - currentOrientation.yaw_deg;
  headingError = headingError - 360 * Math.floor((headingError + 180) / 360);
  altitudeError = targetAlt - currentLocation.altitude_m;

  when {distanceKm < waypointProximity_km, missionDone} then
    if not missionDone then
      if waypointIndex < waypointCount then
        waypointIndex := waypointIndex + 1;
      else
        missionDone := true;
      end if;
    end if;
  end when;

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
