within AdaptiveWingSystemFMU;
model AdaptiveWingSystem
  extends AircraftCommon.AdaptiveWingSystem_Interface;
protected
  Real liftCommand;
  Real speedFactor;
equation
  actuation_command.left_aileron_deg = max(-rollAuthority_deg, min(rollAuthority_deg, direction_command.roll_deg));
  actuation_command.right_aileron_deg = -actuation_command.left_aileron_deg;
  actuation_command.elevator_deg = max(-pitchAuthority_deg, min(pitchAuthority_deg, direction_command.pitch_deg));
  actuation_command.rudder_deg = direction_command.yaw_deg;
  actuation_command.flaperon_deg = 0.5 * actuation_command.elevator_deg;

  speedFactor = max(0.5, min(1.5, flight_speed.airspeed_mps / 200));
  liftCommand = (actuation_command.left_aileron_deg - actuation_command.right_aileron_deg) / (2 * rollAuthority_deg)
              + actuation_command.elevator_deg / (2 * pitchAuthority_deg);
  liftInterface.lift_kn = liftCoeffBase * wingAreaScale * speedFactor * (1 + liftCommand);
  liftInterface.drag_kn = 0.12 * liftInterface.lift_kn;
  liftInterface.pitching_moment_knm = actuation_command.elevator_deg * referenceArea / aspectRatio;
end AdaptiveWingSystem;
