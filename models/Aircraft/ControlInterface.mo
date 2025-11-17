within Aircraft;
model ControlInterface
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real inputLag = 0.05 "Blending factor for pilot input smoothing";
  parameter Real manualCommandDefault(min=0.0, max=1.0) = 0.6 "Nominal throttle stick position";
  output GI.PilotCommand pilotCommand;
protected
  Real effectiveCommand;
  Real rollSweep;
equation
  // Simple smoothing around a nominal throttle input
  effectiveCommand = (1 - inputLag) * manualCommandDefault + inputLag * manualCommandDefault;
  rollSweep = 0.2 * sin(time / 5);
  pilotCommand.stick_pitch_norm = min(1.0, max(-1.0, (effectiveCommand - 0.5) * 2));
  pilotCommand.stick_roll_norm = rollSweep;
  pilotCommand.rudder_norm = 0.1 * rollSweep;
  pilotCommand.throttle_norm = min(1.0, max(0.0, effectiveCommand));
  pilotCommand.throttle_aux_norm = pilotCommand.throttle_norm;
  pilotCommand.button_mask = 0;
  pilotCommand.hat_x = 0;
  pilotCommand.hat_y = 0;
  pilotCommand.mode_switch = 0;
  pilotCommand.reserved = 0;
end ControlInterface;
