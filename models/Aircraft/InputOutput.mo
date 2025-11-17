within Aircraft;
model InputOutput
  import GI = Aircraft.GeneratedInterfaces;
  input GI.GeodeticLLA locationLLA;
  input GI.OrientationEuler orientation;
  input GI.MissionStatus missionStatus;
  input GI.PilotCommand autopilotCmd;
  input GI.AutonomyGuidance guidance;
  input GI.FlightStatusPacket flightStatus;
end InputOutput;
