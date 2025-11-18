within Aircraft;
model InputOutput
  import GI = Aircraft.GeneratedInterfaces;
  input GI.PositionXYZ locationXYZ;
  input GI.OrientationEuler orientation;
  input GI.MissionStatus missionStatus;
  input GI.PilotCommand autopilotCmd;
  input GI.FlightStatusPacket flightStatus;
end InputOutput;
