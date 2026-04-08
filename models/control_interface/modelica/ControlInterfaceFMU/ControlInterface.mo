within ControlInterfaceFMU;
model ControlInterface
  import GI = AircraftCommon.GeneratedInterfaces;
  parameter Boolean useBridgeInput = false "Prefer external bridge/manual command input";
  parameter Real inputLag = 0.05 "Blending factor for pilot input smoothing";
  parameter Real manualCommandDefault(min=0.0, max=1.0) = 0.6 "Nominal throttle stick position";
  input GI.PilotCommand bridgeInput;
  output GI.PilotCommand pilotCommand;
protected
  Real effectiveCommand;
  Real rollSweep;
  Boolean bridgeActive;
  GI.PilotCommand scriptedPilotCommand;
equation
  effectiveCommand = (1 - inputLag) * manualCommandDefault + inputLag * manualCommandDefault;
  rollSweep = 0.2 * sin(time / 5);
  scriptedPilotCommand.stick_pitch_norm = min(1.0, max(-1.0, (effectiveCommand - 0.5) * 2));
  scriptedPilotCommand.stick_roll_norm = rollSweep;
  scriptedPilotCommand.rudder_norm = 0.1 * rollSweep;
  scriptedPilotCommand.throttle_norm = min(1.0, max(0.0, effectiveCommand));
  scriptedPilotCommand.throttle_aux_norm = scriptedPilotCommand.throttle_norm;
  scriptedPilotCommand.button_mask = 0;
  scriptedPilotCommand.hat_x = 0;
  scriptedPilotCommand.hat_y = 0;
  scriptedPilotCommand.mode_switch = 0;
  scriptedPilotCommand.reserved = 0;
  bridgeActive = useBridgeInput and bridgeInput.mode_switch >= 0;

  pilotCommand.stick_pitch_norm = if bridgeActive then bridgeInput.stick_pitch_norm else scriptedPilotCommand.stick_pitch_norm;
  pilotCommand.stick_roll_norm = if bridgeActive then bridgeInput.stick_roll_norm else scriptedPilotCommand.stick_roll_norm;
  pilotCommand.rudder_norm = if bridgeActive then bridgeInput.rudder_norm else scriptedPilotCommand.rudder_norm;
  pilotCommand.throttle_norm = if bridgeActive then bridgeInput.throttle_norm else scriptedPilotCommand.throttle_norm;
  pilotCommand.throttle_aux_norm = if bridgeActive then bridgeInput.throttle_aux_norm else scriptedPilotCommand.throttle_aux_norm;
  pilotCommand.button_mask = if bridgeActive then bridgeInput.button_mask else scriptedPilotCommand.button_mask;
  pilotCommand.hat_x = if bridgeActive then bridgeInput.hat_x else scriptedPilotCommand.hat_x;
  pilotCommand.hat_y = if bridgeActive then bridgeInput.hat_y else scriptedPilotCommand.hat_y;
  pilotCommand.mode_switch = if bridgeActive then bridgeInput.mode_switch else scriptedPilotCommand.mode_switch;
  pilotCommand.reserved = if bridgeActive then bridgeInput.reserved else scriptedPilotCommand.reserved;
end ControlInterface;
