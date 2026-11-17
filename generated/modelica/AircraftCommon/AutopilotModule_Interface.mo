within AircraftCommon;

partial model AutopilotModule_Interface
  parameter Real updateRateHz = 40;
  parameter Real defaultThrottle = 0.5;
  parameter Real targetAirspeed_mps = 200;
  parameter Real airspeedToThrottleGain = 0.003;
  parameter Real climbRateToThrottleGain = 0.001;
  parameter Real minThrottleCommand = 0.2;
  parameter Real headingGain = 0.016666666666666666;
  parameter Real altitudeToPitchGain = 10;
  parameter Real pitchAngleGain = 0.05;
  parameter Real maxPitchCommand_deg = 20;
  parameter Real waypointX_km[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  parameter Real waypointY_km[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  parameter Real waypointZ_km[10] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
  parameter Real waypointProximity_km = 10;
  parameter Real waypointAltitudeProximity_km = 1;
  parameter Real tauCmd = 1;
  input GeneratedInterfaces.FlightStatusPacket feedbackBus;
  input GeneratedInterfaces.PositionXYZ currentLocation;
  input GeneratedInterfaces.OrientationEuler currentOrientation;
  output GeneratedInterfaces.PilotCommand autopilotCmd;
  output GeneratedInterfaces.MissionStatus missionStatus;
end AutopilotModule_Interface;
