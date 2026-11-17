within AircraftCommon;

partial model AdaptiveWingSystem_Interface
  parameter Real referenceArea = 28;
  parameter Real span = 10;
  parameter Real aspectRatio = 3.6;
  parameter Real wingAreaScale = 1;
  parameter Real liftCoeffBase = 0.75;
  parameter Real liftSlopePerDeg = 0.05;
  parameter Real dragCoeffBase = 0.05;
  parameter Real dragSlopePerDeg = 0.01;
  parameter Real pitchMomentGain = 0.1;
  parameter Real pitchMomentNormalizer_deg = 20;
  parameter Real rollAuthority_deg = 25;
  parameter Real pitchAuthority_deg = 20;
  input GeneratedInterfaces.OrientationEuler direction_command;
  input GeneratedInterfaces.FlightStatusPacket flight_speed;
  output GeneratedInterfaces.SurfaceActuationCommand actuation_command;
  output GeneratedInterfaces.LiftState liftInterface;
end AdaptiveWingSystem_Interface;
