within AircraftCommon;

partial model Environment_Interface
  parameter Real initX_km = 0;
  parameter Real initY_km = 0;
  parameter Real initZ_km = 1;
  parameter Real tauDirection_s = 2;
  parameter Real thrustToSpeedGain = 4;
  parameter Real climbBleedFraction = 0.35;
  parameter Real minAirspeed_mps = 50;
  parameter Real referenceEnergySpeed_mps = 300;
  input GeneratedInterfaces.SurfaceActuationCommand actuation_command;
  input GeneratedInterfaces.OrientationEuler direction_command;
  input GeneratedInterfaces.LiftState lift;
  input GeneratedInterfaces.ThrustState thrust_in;
  output GeneratedInterfaces.OrientationEuler orientation;
  output GeneratedInterfaces.PositionXYZ location;
  output GeneratedInterfaces.FlightStatusPacket flight_status;
end Environment_Interface;
