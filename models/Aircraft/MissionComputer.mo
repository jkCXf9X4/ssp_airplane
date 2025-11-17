within Aircraft;
model MissionComputer
  import GI = Aircraft.GeneratedInterfaces;
  parameter Integer flyByWireChannels = 3;
  parameter Real computeBudgetTOPS = 35;
  parameter Integer storesBuses = 2;
  input GI.PilotCommand manualInput;
  input GI.PilotCommand autopilotInput;
  input GI.MissionStatus autopilotStatus;
  input GI.AutonomyGuidance autonomyPort;
  input GI.AirDataInertialState airDataIn;
  input GI.GenericElectricalBus powerIn;
  input GI.GenericElectricalBus backupPower;
  input GI.FuelLevelState fuelStatus;
  input GI.StoresStatusBus storesStatus;
  input GI.StructuralPerformanceState performanceStatus;
  output GI.ThrottleCommand engineThrottle;
  output GI.SurfaceActuationCommand surfaceBus;
  output GI.FlightStatusPacket flightStatus;
  output GI.OrientationEuler orientationEuler;
  output GI.GeodeticLLA locationLLA;
  output GI.StoresCommandBus storesCommand;
protected
  Real blendCmd;
  Real powerFactor;
  Real headingDeg(start=0);
  Real positionKm(start=0);
  parameter Real headingGain = 75;
  parameter Real velocityGain = 230;
  Boolean autopilotEngaged;
  Real cmdStickRoll;
  Real cmdStickPitch;
  Real cmdRudder;
  Real cmdThrottle;
  Real cmdThrottleAux;
  Integer cmdButtonMask;
  Integer cmdHatX;
  Integer cmdHatY;
  Integer cmdModeSwitch;
  Real manualScalar;
  Real autonomyScalar;
  Real electricalScalar;
  Real fuelScalar;
  Real fbwAuthority;
  Real loadLimiter;
  Real storesReadyRatio;
  Real measuredAirspeed;
  Boolean releaseEnable;
  Integer presentMask;
equation
  autopilotEngaged = autopilotInput.mode_switch > 0;

  cmdStickRoll = if autopilotEngaged then autopilotInput.stick_roll_norm else manualInput.stick_roll_norm;
  cmdStickPitch = if autopilotEngaged then autopilotInput.stick_pitch_norm else manualInput.stick_pitch_norm;
  cmdRudder = if autopilotEngaged then autopilotInput.rudder_norm else manualInput.rudder_norm;
  cmdThrottle = if autopilotEngaged then autopilotInput.throttle_norm else manualInput.throttle_norm;
  cmdThrottleAux = if autopilotEngaged then autopilotInput.throttle_aux_norm else manualInput.throttle_aux_norm;
  cmdButtonMask = if autopilotEngaged then autopilotInput.button_mask else manualInput.button_mask;
  cmdHatX = if autopilotEngaged then autopilotInput.hat_x else manualInput.hat_x;
  cmdHatY = if autopilotEngaged then autopilotInput.hat_y else manualInput.hat_y;
  cmdModeSwitch = if autopilotEngaged then autopilotInput.mode_switch else manualInput.mode_switch;

  manualScalar = min(1.0, max(0.0, cmdThrottle));
  autonomyScalar = min(1.0, max(0.0, autonomyPort.aggressiveness_norm));
  electricalScalar = min(1.0, max(0.2, (powerIn.available_power_kw + 0.5 * backupPower.available_power_kw) / 80.0));
  fuelScalar = min(1.0, max(0.0, fuelStatus.fuel_level_norm));
  fbwAuthority = min(1.0, flyByWireChannels / 3.0);
  loadLimiter = min(1.0, max(0.2, performanceStatus.structural_margin_norm));
  storesReadyRatio = if storesStatus.store_present_mask > 0 then min(1.0, max(0.0, storesStatus.weapon_ready_mask / max(1.0, storesStatus.store_present_mask))) else 1.0;
  measuredAirspeed = if airDataIn.true_airspeed_mps > 0 then airDataIn.true_airspeed_mps else 250 * manualScalar;
  releaseEnable = cmdButtonMask > 0 and not performanceStatus.stores_release_inhibit;
  presentMask = if storesStatus.store_present_mask > 0 then storesStatus.store_present_mask else 511;

  blendCmd = 0.5 * autonomyScalar + 0.5 * manualScalar;
  powerFactor = electricalScalar * fuelScalar * loadLimiter;
  engineThrottle.throttle_norm = min(1.0, max(0.12, blendCmd * powerFactor * fbwAuthority));
  engineThrottle.fuel_enable = not fuelStatus.fuel_starved;
  engineThrottle.afterburner_enable = engineThrottle.throttle_norm > 0.85 and cmdThrottleAux > 0.5;

  surfaceBus.left_aileron_deg = 12 * (cmdStickRoll);
  surfaceBus.right_aileron_deg = -surfaceBus.left_aileron_deg;
  surfaceBus.elevator_deg = 12 * cmdStickPitch;
  surfaceBus.rudder_deg = 7 * cmdRudder;
  surfaceBus.flaperon_deg = 6 * (engineThrottle.throttle_norm - 0.5);

  flightStatus.airspeed_mps = measuredAirspeed;
  flightStatus.energy_state_norm = fuelScalar * electricalScalar;
  flightStatus.angle_of_attack_deg = airDataIn.angle_of_attack_deg;
  flightStatus.health_code = if fuelStatus.fuel_starved then 2 else if electricalScalar < 0.4 then 1 else storesBuses;

  der(headingDeg) = headingGain * (cmdStickRoll / 2) + 20 * (autonomyScalar - 0.5);
  der(positionKm) = velocityGain * engineThrottle.throttle_norm;

  orientationEuler.roll_deg = surfaceBus.left_aileron_deg - surfaceBus.right_aileron_deg;
  orientationEuler.pitch_deg = airDataIn.angle_of_attack_deg;
  orientationEuler.yaw_deg = headingDeg;

  locationLLA.latitude_deg = positionKm / 111.0;
  locationLLA.longitude_deg = 0.0;
  locationLLA.altitude_m = 0.5 * autonomyPort.waypoint_altitude_m + 0.5 * airDataIn.pressure_altitude_m;

  storesCommand.selected_station = 1 + integer(mod(time, 9));
  storesCommand.release_enable = releaseEnable;
  storesCommand.pickle_command = releaseEnable and (cmdModeSwitch == 1 or storesReadyRatio > 0.8);
  storesCommand.jettison_all = cmdModeSwitch == 3;
  storesCommand.power_mode_mask = presentMask;
  storesCommand.config_checksum = presentMask + storesStatus.weapon_ready_mask;
end MissionComputer;
