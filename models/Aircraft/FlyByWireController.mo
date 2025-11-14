within Aircraft;
model FlyByWireController
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real updateRateHz = 200;
  parameter Real authorityDefault = 0.85;
  input GI.SurfaceActuationCommand commandBus;
  input GI.FlightStatusPacket flightFeedback;
  input GI.LiftState aeroFeedback;
  input GI.GenericElectricalBus powerIn;
  output GI.SurfaceActuationCommand actuatorDrive;
protected
  Real authority;
  Real damping;
  Real trimBias;
equation
  authority = min(1.0, max(0.2, authorityDefault * powerIn.available_power_kw / 40.0));
  damping = min(1.0, max(0.3, 1 - aeroFeedback.drag_kn / max(1, aeroFeedback.lift_kn + 1)));
  trimBias = max(-5, min(5, flightFeedback.angle_of_attack_deg / 3));

  actuatorDrive.left_aileron_deg = authority * damping * commandBus.left_aileron_deg;
  actuatorDrive.right_aileron_deg = authority * damping * commandBus.right_aileron_deg;
  actuatorDrive.elevator_deg = authority * (commandBus.elevator_deg - trimBias);
  actuatorDrive.rudder_deg = authority * commandBus.rudder_deg;
  actuatorDrive.flaperon_deg = authority * commandBus.flaperon_deg;
end FlyByWireController;
