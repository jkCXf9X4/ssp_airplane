within WingmanDrone;
model ControlInterface
  import GI = WingmanDrone.GeneratedInterfaces;
  parameter Real inputLag = 0.15;
  parameter Real manualCommandDefault(min=0.0, max=1.0) = 0.5;
  input GI.GenericElectricalBus powerIn;
  output GI.PilotCommand pilotCommand;
protected
  Real effectiveCommand;
equation
  effectiveCommand = (1 - inputLag) * manualCommandDefault + inputLag * min(1.0, max(0.0, powerIn.available_power_kw / 100.0));
  pilotCommand.stick_pitch_norm = min(1.0, max(-1.0, effectiveCommand - 0.5) * 2);
  pilotCommand.stick_roll_norm = 0.0;
  pilotCommand.rudder_norm = 0.0;
  pilotCommand.throttle_norm = min(1.0, max(0.0, effectiveCommand));
  pilotCommand.throttle_aux_norm = pilotCommand.throttle_norm;
  pilotCommand.button_mask = 0;
  pilotCommand.hat_x = 0;
  pilotCommand.hat_y = 0;
  pilotCommand.mode_switch = 0;
  pilotCommand.reserved = 0;
end ControlInterface;
