within Aircraft;
model AutopilotModule
  import GI = Aircraft.GeneratedInterfaces;
  import Modelica.Constants;
  import Modelica.Math;

  constant Real degToRad = Constants.pi / 180;
  constant Real radToDeg = 180 / Constants.pi;
  parameter Real updateRateHz = 40;
  parameter Real defaultThrottle = 0.7;
  parameter Real headingGain = 1 / 60.0 "deg^-1 to normalize yaw error into stick roll";
  parameter Real altitudeGain = 1 / 3.0 "m^-1 to normalize altitude error into stick pitch";

  parameter Integer waypointCount = 10;
  parameter Real waypointX_km[waypointCount] = fill(0.0, waypointCount);
  parameter Real waypointY_km[waypointCount] = fill(0.0, waypointCount);
  parameter Real waypointZ_km[waypointCount] = fill(1, waypointCount);
  parameter Real waypointProximity_km = 10 "Distance to trigger waypoint switch";
  // time constant for smoothing
  parameter Real tauCmd = 1.0 "s, command filter time constant";

  input GI.FlightStatusPacket feedbackBus;
  input GI.PositionXYZ currentLocation;
  input GI.OrientationEuler currentOrientation;
  output GI.PilotCommand autopilotCmd;
  output GI.MissionStatus missionStatus;
protected
  Integer activeWaypoint;
  Real headingError;
  Real dx_km;
  Real dy_km;
  Real dz_km;
  Real currentX_km;
  Real currentY_km;
  Real currentZ_km;
  Real targetX_km;
  Real targetY_km;
  Real targetZ_km;
  Real altitudeError;
  Real holdStrength;
  Real targetHeading;
  Real distanceToWaypoint_km;
  Boolean arrived;
  Integer waypointIndex(start=1, fixed=true);
  Boolean missionDone(start=false, fixed=true);

  // “raw” commands directly from control laws
  Real rollCmd_raw;
  Real pitchCmd_raw;
  Real throttleCmd_raw;

  // filtered commands that go to the outputs
  Real rollCmd(start=0);
  Real pitchCmd(start=0);
  Real throttleCmd(start=defaultThrottle);

equation
  // Pick the active waypoint (clamp to the configured list to avoid indexing beyond the end)
  activeWaypoint = if waypointCount < 1 then 1 else min(waypointIndex, waypointCount);

  // Current position in already-projected x/y/z kilometers (supplied by environment)
  currentX_km = currentLocation.x_km;
  currentY_km = currentLocation.y_km;
  currentZ_km = currentLocation.z_km;

  targetX_km = waypointX_km[pre(activeWaypoint)];
  targetY_km = waypointY_km[pre(activeWaypoint)];
  targetZ_km = waypointZ_km[pre(activeWaypoint)];

  dx_km = targetX_km - currentX_km;
  dy_km = targetY_km - currentY_km;
  dz_km = targetZ_km - currentZ_km;

  distanceToWaypoint_km = if waypointCount < 1 then 0 else sqrt(dx_km ^ 2 + dy_km ^ 2 + dz_km ^ 2);
  targetHeading = if waypointCount < 1 then currentOrientation.yaw_deg else Math.atan2(dy_km, dx_km) * radToDeg;

  // Normalize heading error into [-180, 180] to avoid commanding a long turn the wrong direction
  headingError = Math.atan2(
    Math.sin((targetHeading - currentOrientation.yaw_deg) * degToRad),
    Math.cos((targetHeading - currentOrientation.yaw_deg) * degToRad)) * radToDeg;

  altitudeError = if waypointCount < 1 then 1 - currentZ_km else dz_km;
  holdStrength = max(0.2, min(1.0, defaultThrottle * max(0.2, feedbackBus.energy_state_norm)));

  // raw commands with saturation (use noEvent to avoid extra events)
  rollCmd_raw    = noEvent(max(-1.0, min(1.0, headingGain  * headingError)));
  pitchCmd_raw   = noEvent(max(-1.0, min(1.0, altitudeGain * altitudeError)));
  throttleCmd_raw = holdStrength; // already 0.2..1.0

  // first-order low-pass filters: der(x) = (u - x)/tau
  der(rollCmd)    = (rollCmd_raw    - rollCmd)    / tauCmd;
  der(pitchCmd)   = (pitchCmd_raw   - pitchCmd)   / tauCmd;
  der(throttleCmd)= (throttleCmd_raw- throttleCmd)/ tauCmd;
  
  arrived = waypointCount > 0 and distanceToWaypoint_km <= waypointProximity_km;

  missionStatus.total_waypoints = waypointCount;
  missionStatus.waypoint_index = if waypointCount < 1 then 0 else waypointIndex;
  missionStatus.distance_to_waypoint_km = distanceToWaypoint_km;
  missionStatus.arrived = arrived;
  missionStatus.complete = missionDone;

  autopilotCmd.stick_roll_norm   = rollCmd;
  autopilotCmd.stick_pitch_norm  = pitchCmd;
  autopilotCmd.throttle_norm     = throttleCmd;
  autopilotCmd.throttle_aux_norm = throttleCmd;
  autopilotCmd.rudder_norm = autopilotCmd.stick_roll_norm / 2;
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