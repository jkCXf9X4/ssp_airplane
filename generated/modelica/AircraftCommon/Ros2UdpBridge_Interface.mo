within AircraftCommon;

partial model Ros2UdpBridge_Interface
  parameter String transport = "Ros2UdpBridge";
  parameter Real reference_latitude_deg = 0;
  parameter Real reference_longitude_deg = 0;
  parameter Real reference_altitude_m = 0;
  parameter String remote_host = "127.0.0.1";
  parameter Integer telemetry_port = 5501;
  parameter Integer control_port = 5502;
  input GeneratedInterfaces.PositionXYZ statePosition;
  input GeneratedInterfaces.OrientationEuler stateOrientation;
  input GeneratedInterfaces.FlightStatusPacket flightStatus;
  input GeneratedInterfaces.MissionStatus missionStatus;
  output GeneratedInterfaces.PilotCommand pilotCommand;
end Ros2UdpBridge_Interface;
