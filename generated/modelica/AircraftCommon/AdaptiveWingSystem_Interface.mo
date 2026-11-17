within AircraftCommon;

partial model AdaptiveWingSystem_Interface
  parameter Real reference_area_m2 = 28;
  parameter Real span_m = 10;
  parameter Real aspect_ratio = 3.6;
  parameter Real control_authority_deg = 25;
  parameter Integer load_factor_limit_g = 9;
  parameter Real referenceArea = 28;
  parameter Real span = 10;
  parameter Real wingAreaScale = 1;
  parameter Real aspectRatio = 3.6;
  parameter Real liftCoeffBase = 0.75;
  parameter Real rollAuthority_deg = 25;
  parameter Real pitchAuthority_deg = 20;
  input GeneratedInterfaces.OrientationEuler direction_command;
  input GeneratedInterfaces.FlightStatusPacket flight_speed;
  output GeneratedInterfaces.SurfaceActuationCommand actuation_command;
  output GeneratedInterfaces.LiftState liftInterface;
end AdaptiveWingSystem_Interface;
