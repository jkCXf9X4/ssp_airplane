within WingmanDrone;
model MissionComputer
  import GI = WingmanDrone.GeneratedInterfaces;
  parameter Real redundancyLevel = 3;
  parameter Real computeBudgetTOPS = 25;
  input GI.PilotCommandOut manualInput;
  input GI.AutonomyGuidance autonomyPort;
  input GI.ElectricalBusState powerIn;
  input GI.FuelLevelState fuelStatus;
  output GI.ThrottleCommand engineThrottle;
  output GI.SurfaceActuationCommand surfaceBus;
  output GI.FlightStatusPacket flightStatus;
  output GI.OrientationEuler orientationEuler;
  output GI.GeodeticLLA locationLLA;
protected
  Real blendCmd;
  Real powerFactor;
  Real headingDeg(start=0);
  Real positionKm(start=0);
  parameter Real headingGain = 60;
  parameter Real velocityGain = 180;
  Real manualScalar;
  Real autonomyScalar;
  Real electricalScalar;
  Real fuelScalar;
equation
  manualScalar = min(1.0, max(0.0, manualInput.throttle_norm));
  autonomyScalar = min(1.0, max(0.0, autonomyPort.aggressiveness_norm));
  electricalScalar = min(1.0, max(0.2, powerIn.available_power_kw / 100.0));
  fuelScalar = min(1.0, max(0.0, fuelStatus.fuel_level_norm));

  blendCmd = 0.6 * autonomyScalar + 0.4 * manualScalar;
  powerFactor = electricalScalar * fuelScalar;
  engineThrottle.throttle_norm = min(1.0, max(0.1, blendCmd * powerFactor));
  engineThrottle.fuel_enable = not fuelStatus.fuel_starved;
  engineThrottle.afterburner_enable = engineThrottle.throttle_norm > 0.9;

  surfaceBus.left_aileron_deg = 10 * (manualInput.stick_roll_norm);
  surfaceBus.right_aileron_deg = -surfaceBus.left_aileron_deg;
  surfaceBus.elevator_deg = 8 * manualInput.stick_pitch_norm;
  surfaceBus.rudder_deg = 5 * manualInput.rudder_norm;
  surfaceBus.flaperon_deg = 4 * (engineThrottle.throttle_norm - 0.5);

  flightStatus.airspeed_mps = 200 * engineThrottle.throttle_norm;
  flightStatus.energy_state_norm = fuelScalar;
  flightStatus.angle_of_attack_deg = surfaceBus.elevator_deg / 4;
  flightStatus.health_code = if fuelStatus.fuel_starved then 1 else 0;

  der(headingDeg) = headingGain * (manualInput.stick_roll_norm / 2) + 20 * (autonomyScalar - 0.5);
  der(positionKm) = velocityGain * engineThrottle.throttle_norm;

  orientationEuler.roll_deg = surfaceBus.left_aileron_deg - surfaceBus.right_aileron_deg;
  orientationEuler.pitch_deg = surfaceBus.elevator_deg;
  orientationEuler.yaw_deg = headingDeg;

  locationLLA.latitude_deg = positionKm / 111.0;
  locationLLA.longitude_deg = 0.0;
  locationLLA.altitude_m = autonomyPort.waypoint_altitude_m;
end MissionComputer;
