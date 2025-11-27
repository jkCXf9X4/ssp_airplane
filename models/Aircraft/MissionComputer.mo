within Aircraft;
model MissionComputer
  import GI = Aircraft.GeneratedInterfaces;
  parameter Integer flyByWireChannels = 3;
  parameter Real rollAuthority_deg = 25;
  parameter Real pitchAuthority_deg = 20;
  parameter Real yawAuthority_deg = 10;
  input GI.PilotCommand manualInput;
  input GI.PilotCommand autopilotInput;
  input GI.FuelLevelState fuelStatus;
  output GI.ThrottleCommand engineThrottle;
  output GI.OrientationEuler direction_command;
protected
  Boolean autopilotEngaged;
  Real stateKeeper(start=0) "Dummy continuous state to satisfy co-sim master";
  Real cmdStickRoll;
  Real cmdStickPitch;
  Real cmdRudder;
  Real cmdThrottle;
  Real cmdThrottleAux;
  Integer cmdModeSwitch;
equation
  autopilotEngaged = autopilotInput.mode_switch > 0;

  cmdStickRoll = if autopilotEngaged then autopilotInput.stick_roll_norm else manualInput.stick_roll_norm;
  cmdStickPitch = if autopilotEngaged then autopilotInput.stick_pitch_norm else manualInput.stick_pitch_norm;
  cmdRudder = if autopilotEngaged then autopilotInput.rudder_norm else manualInput.rudder_norm;
  cmdThrottle = if autopilotEngaged then autopilotInput.throttle_norm else manualInput.throttle_norm;
  cmdThrottleAux = if autopilotEngaged then autopilotInput.throttle_aux_norm else manualInput.throttle_aux_norm;
  cmdModeSwitch = if autopilotEngaged then autopilotInput.mode_switch else manualInput.mode_switch;

  engineThrottle.throttle_norm = min(1.0, max(0.12, cmdThrottle));
  engineThrottle.fuel_enable = not fuelStatus.fuel_starved;
  engineThrottle.afterburner_enable = engineThrottle.throttle_norm > 0.85 and cmdThrottleAux > 0.5;

  direction_command.roll_deg = rollAuthority_deg * cmdStickRoll;
  direction_command.pitch_deg = pitchAuthority_deg * cmdStickPitch;
  direction_command.yaw_deg = yawAuthority_deg * cmdRudder;

  // Keep at least one continuous state so the FMU tolerates master calls to getContinuousStates
  der(stateKeeper) = 0;
end MissionComputer;
