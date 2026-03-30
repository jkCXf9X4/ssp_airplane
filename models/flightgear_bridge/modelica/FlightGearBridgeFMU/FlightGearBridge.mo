within FlightGearBridgeFMU;
model FlightGearBridge
  import GI = AircraftCommon.GeneratedInterfaces;

  parameter String transport = "FlightGearGeneric" "Bridge transport/profile identifier";
  parameter Real referenceLatitude_deg = 0.0 "Visualization origin latitude";
  parameter Real referenceLongitude_deg = 0.0 "Visualization origin longitude";
  parameter Real referenceAltitude_m = 0.0 "Visualization origin altitude";

  parameter Real commandStickPitch = 0.0 "Default bridge pitch command";
  parameter Real commandStickRoll = 0.0 "Default bridge roll command";
  parameter Real commandRudder = 0.0 "Default bridge rudder command";
  parameter Real commandThrottle = 0.6 "Default bridge throttle command";
  parameter Real commandThrottleAux = 0.6 "Default bridge auxiliary throttle command";
  parameter Integer commandModeSwitch = 0 "0=manual, 1+=autopilot/assist modes";

  input GI.PositionXYZ statePosition;
  input GI.OrientationEuler stateOrientation;
  input GI.FlightStatusPacket flightStatus;
  input GI.MissionStatus missionStatus;

  output GI.PilotCommand pilotCommand;
equation
  // Placeholder adapter model. The first runtime implementation will externalize
  // the FlightGear socket exchange while preserving these signals/parameters.
  pilotCommand.stick_pitch_norm = commandStickPitch;
  pilotCommand.stick_roll_norm = commandStickRoll;
  pilotCommand.rudder_norm = commandRudder;
  pilotCommand.throttle_norm = commandThrottle;
  pilotCommand.throttle_aux_norm = commandThrottleAux;
  pilotCommand.button_mask = 0;
  pilotCommand.hat_x = 0;
  pilotCommand.hat_y = 0;
  pilotCommand.mode_switch = commandModeSwitch;
  pilotCommand.reserved = 0;
end FlightGearBridge;
