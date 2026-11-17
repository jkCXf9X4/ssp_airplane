within AircraftCommon;

partial model ControlInterface_Interface
  parameter String input_scheme = "HOTAS";
  parameter Integer telemetry_rate_hz = 120;
  parameter Boolean useBridgeInput = false;
  parameter Real inputLag = 0.05;
  parameter Real manualCommandDefault = 0.6;
  input GeneratedInterfaces.PilotCommand bridgeInput;
  output GeneratedInterfaces.PilotCommand pilotCommand;
end ControlInterface_Interface;
