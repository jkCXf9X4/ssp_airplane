within AircraftCommon;

partial model MissionComputer_Interface
  parameter Integer flyByWireChannels = 3;
  parameter Real rollAuthority_deg = 25;
  parameter Real pitchAuthority_deg = 20;
  parameter Real yawAuthority_deg = 10;
  input GeneratedInterfaces.PilotCommand manualInput;
  input GeneratedInterfaces.PilotCommand autopilotInput;
  input GeneratedInterfaces.FuelLevelState fuelStatus;
  output GeneratedInterfaces.ThrottleCommand engineThrottle;
  output GeneratedInterfaces.OrientationEuler direction_command;
end MissionComputer_Interface;
