within AircraftCommon;

partial model InputOutput_Interface
  input GeneratedInterfaces.PositionXYZ locationXYZ;
  input GeneratedInterfaces.OrientationEuler orientation;
  input GeneratedInterfaces.PilotCommand autopilotCmd;
  input GeneratedInterfaces.FlightStatusPacket flightStatus;
  input GeneratedInterfaces.MissionStatus missionStatus;
end InputOutput_Interface;
