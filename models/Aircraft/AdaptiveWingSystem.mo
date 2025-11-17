within Aircraft;
model AdaptiveWingSystem
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real referenceArea = 28 "m2";
  parameter Real span = 10 "m";
  parameter Real wingAreaScale(min=0.7, max=1.3) = 1.0;
  parameter Real aspectRatio = 3.6;
  parameter Real liftCoeffBase = 0.75;
  parameter Real rollAuthority_deg = 25;
  parameter Real pitchAuthority_deg = 20;
  input GI.OrientationEuler velocity_vector_alteration "desired change from mission computer";
  input GI.FlightStatusPacket flight_speed;
  output GI.SurfaceActuationCommand actuation_command "Commanded surfaces to the environment";
  output GI.LiftState liftInterface;
protected
  Real liftCommand;
  Real speedFactor;
equation
  actuation_command.left_aileron_deg = max(-rollAuthority_deg, min(rollAuthority_deg, velocity_vector_alteration.roll_deg));
  actuation_command.right_aileron_deg = -actuation_command.left_aileron_deg;
  actuation_command.elevator_deg = max(-pitchAuthority_deg, min(pitchAuthority_deg, velocity_vector_alteration.pitch_deg));
  actuation_command.rudder_deg = velocity_vector_alteration.yaw_deg;
  actuation_command.flaperon_deg = 0.5 * actuation_command.elevator_deg;

  speedFactor = max(0.5, min(1.5, flight_speed.airspeed_mps / 200));
  liftCommand = (actuation_command.left_aileron_deg - actuation_command.right_aileron_deg) / (2 * rollAuthority_deg)
              + actuation_command.elevator_deg / (2 * pitchAuthority_deg);
  liftInterface.lift_kn = liftCoeffBase * wingAreaScale * speedFactor * (1 + liftCommand);
  liftInterface.drag_kn = 0.12 * liftInterface.lift_kn;
  liftInterface.pitching_moment_knm = actuation_command.elevator_deg * referenceArea / aspectRatio;
end AdaptiveWingSystem;
