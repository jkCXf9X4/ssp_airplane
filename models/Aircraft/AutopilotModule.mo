within Aircraft;
model AutopilotModule
  import GI = Aircraft.GeneratedInterfaces;
  import Modelica.Constants;
  import Modelica.Math;

  constant Real degToRad = Constants.pi / 180;
  constant Real radToDeg = 180 / Constants.pi;
  parameter Real updateRateHz = 40;
  parameter Real sensorFidelity = 0.98;
  parameter Real defaultThrottle = 0.7;
  parameter Real headingGain = 1 / 60.0 "deg^-1 to normalize yaw error into stick roll";
  parameter Real altitudeGain = 1 / 3000.0 "m^-1 to normalize altitude error into stick pitch";
  parameter Real targetAltitude_m = 6000;

  parameter Integer waypointCount = 10;
  parameter Real waypointLat[waypointCount] = fill(0.0, waypointCount);
  parameter Real waypointLon[waypointCount] = fill(0.0, waypointCount);
  parameter Real waypointAlt[waypointCount] = fill(targetAltitude_m, waypointCount);
  parameter Real waypointProximity_km = 10 "Distance to trigger waypoint switch";

  input GI.FlightStatusPacket feedbackBus;
  input GI.GeodeticLLA currentLocation;
  input GI.OrientationEuler currentOrientation;
  output GI.PilotCommand autopilotCmd;
  output GI.MissionStatus missionStatus;
protected
  Integer activeWaypoint;
  Real headingError;
  Real altitudeError;
  Real holdStrength;
  Real targetHeading;
  Real targetAltitude;
  Real distanceToWaypoint_km;
  Boolean arrived;
  Integer waypointIndex(start=1, fixed=true);
  Boolean missionDone(start=false, fixed=true);
equation
  // Pick the active waypoint (clamp to the configured list to avoid indexing beyond the end)
  activeWaypoint = if waypointCount < 1 then 1 else min(waypointIndex, waypointCount);

  // Flat-earth approximation: convert longitude delta by cos(latitude) and compute bearing to target
  distanceToWaypoint_km = if waypointCount < 1 then 0 else 111.0 * Math.sqrt(
    (waypointLat[activeWaypoint] - currentLocation.latitude_deg) ^ 2
     + (Math.cos(currentLocation.latitude_deg * degToRad) * (waypointLon[activeWaypoint] - currentLocation.longitude_deg)) ^ 2);
  targetHeading = if waypointCount < 1 then currentOrientation.yaw_deg else Math.atan2(
    Math.cos(currentLocation.latitude_deg * degToRad) * (waypointLon[activeWaypoint] - currentLocation.longitude_deg),
    waypointLat[activeWaypoint] - currentLocation.latitude_deg) * radToDeg;

  // Normalize heading error into [-180, 180] to avoid commanding a long turn the wrong direction
  headingError = Math.atan2(
    Math.sin((targetHeading - currentOrientation.yaw_deg) * degToRad),
    Math.cos((targetHeading - currentOrientation.yaw_deg) * degToRad)) * radToDeg;

  targetAltitude = if waypointCount < 1 then targetAltitude_m else waypointAlt[activeWaypoint];
  altitudeError = targetAltitude - currentLocation.altitude_m;
  holdStrength = max(0.2, min(1.0, defaultThrottle * sensorFidelity * max(0.2, feedbackBus.energy_state_norm)));

  arrived = waypointCount > 0 and distanceToWaypoint_km <= waypointProximity_km;

  missionStatus.total_waypoints = waypointCount;
  missionStatus.waypoint_index = if waypointCount < 1 then 0 else waypointIndex;
  missionStatus.distance_to_waypoint_km = distanceToWaypoint_km;
  missionStatus.arrived = arrived;
  missionStatus.complete = missionDone;

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

algorithm
  // Advance to the next waypoint when we get within the proximity threshold.
  when initial() then
    missionDone := waypointCount < 1;
  elsewhen arrived and waypointIndex < waypointCount then
    waypointIndex := pre(waypointIndex) + 1;
  end when;

  when arrived and waypointIndex >= waypointCount then
    missionDone := true;
  end when;
end AutopilotModule;
